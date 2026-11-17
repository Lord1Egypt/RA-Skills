#!/usr/bin/env python3
"""Build first, then replace only a service recorded by this tool.

--port diagnoses occupancy; it never selects a process to terminate. Commands
must keep the managed service in the foreground, not daemonize or launch and
exit. Records prevent stale-PID accidents, not malicious same-user rewriting.
Build/start run argv with shell=False and a minimal environment. Logs stay in
files and are never echoed automatically. This is not a general process-tree
supervisor, production deployment system, or proof of application correctness.
"""
import argparse
import ipaddress
import math
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.parse import urlsplit

from _contract import guard_endpoint
from _process import (OwnedProcess, canonical, child_env, parse_argv, process_lock,
                      read_record, remove_record, require_process_support,
                      validate_argv, write_record)

SOURCE_EXTS = {'.java', '.kt', '.scala', '.xml', '.yaml', '.yml', '.properties',
               '.py', '.sql', '.json', '.gradle'}
_CHILDREN = {}  # Keep local Popen handles until the owned process is stopped.


def log(message):
    print('[rebuild] ' + message, flush=True)


def newest_source_mtime(project_dir, exclude=()):
    ignored = {canonical(p) for p in exclude}
    newest = 0.0
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in
                   ('target', 'build', 'dist', '.git', '.venv', 'node_modules', '__pycache__')]
        for name in files:
            path = os.path.join(root, name)
            if os.path.splitext(name)[1] in SOURCE_EXTS and canonical(path) not in ignored:
                newest = max(newest, os.path.getmtime(path))
    return newest


def artifact_fresh(artifact, project_dir, exclude=()):
    if not os.path.isfile(artifact):
        return False, 'artifact is absent'
    if newest_source_mtime(project_dir, exclude) > os.path.getmtime(artifact):
        return False, 'artifact is older than project sources'
    return True, 'artifact is current'


def port_occupied(port, host='127.0.0.1'):
    if port is None:
        return False
    family = socket.AF_INET6 if ':' in host else socket.AF_INET
    with socket.socket(family, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((host, port)) == 0


def _loopback_host(host):
    if host == 'localhost':
        return '127.0.0.1'
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return None
    effective = getattr(ip, 'ipv4_mapped', None) or ip
    return str(ip) if effective.is_loopback else None


def stop_service(port=None, pid_file=None, project_dir=None):
    """Compatibility helper: a port never authorizes stopping its listener."""
    if not pid_file or not project_dir:
        if port is not None:
            log('port occupancy: ' + ('occupied' if port_occupied(port) else 'no listener detected'))
        raise ValueError('stopping requires a managed record and project directory')
    record = read_record(pid_file, project_dir)
    if record is None:
        return False
    with OwnedProcess(record['pid']) as process:
        process.verify(record, project_dir)
        process.stop()
    local_child = _CHILDREN.pop(record['pid'], None)
    if local_child is not None:
        local_child.wait(timeout=6)
    remove_record(pid_file, record)
    return True


def wait_ready(health_url, timeout, allow_remote=False, process=None):
    from _network import safe_health
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process is not None and not process.alive():
            return False
        try:
            remaining = deadline - time.monotonic()
            if safe_health(health_url, timeout=max(0.05, min(3, remaining)), allow_remote=allow_remote):
                return process is None or process.alive()
        except ValueError as exc:
            raise ValueError('health check refused: ' + str(exc)) from exc
        except OSError:
            pass
        time.sleep(min(0.1, max(0, deadline - time.monotonic())))
    return False


def _launch_options():
    if os.name == 'nt':
        return {'creationflags': subprocess.CREATE_NO_WINDOW}
    return {'start_new_session': True}


def _cleanup_new(proc, process):
    if process is not None:
        process.stop()
    elif proc is not None and proc.poll() is None:
        # Popen keeps the Windows process handle; on Linux the unreaped child
        # cannot have its PID reused while we acquire the pidfd.
        if os.name == 'nt':
            proc.kill()
        else:
            with OwnedProcess(proc.pid) as child:
                child.stop()
    if proc is not None:
        proc.wait(timeout=6)


def _path(value, project):
    p = Path(value)
    return p.resolve() if p.is_absolute() else (project / p).resolve()


def execute(args):
    require_process_support()
    project = Path(args.project_dir).resolve()
    if not project.is_dir():
        raise ValueError('project directory does not exist')
    pid_file = _path(args.pid_file or '.rebuild-process.json', project)
    if not pid_file.parent.is_dir():
        raise ValueError('process record directory does not exist')
    if args.port is not None and not 1 <= args.port <= 65535:
        raise ValueError('port must be between 1 and 65535')
    with process_lock(pid_file):
        if args.stop:
            stopped = stop_service(args.port, pid_file, project)
            log('owned service stopped' if stopped else 'no managed record; no process stopped')
            return 0
        if not args.artifact or not args.health_url:
            raise ValueError('start requires artifact and health-url')
        if not all(math.isfinite(value) and value > 0 for value in (args.timeout, args.build_timeout)):
            raise ValueError('timeouts must be positive')
        guard_endpoint(args.health_url, args.allow_remote)
        from _network import safe_health  # Import before building or touching the old service.
        env = child_env(args.pass_env)
        start = validate_argv(parse_argv(args.start_cmd, args.start_argv), project, env)
        build = None if args.skip_build else validate_argv(parse_argv(args.build_cmd, args.build_argv), project, env)
        artifact = _path(args.artifact, project)
        log_path = _path(args.log_file or 'service.log', project)
        build_log = _path(args.build_log_file or 'build.log', project)
        if any(not p.parent.is_dir() for p in (log_path, build_log)):
            raise ValueError('log directory does not exist')
        if any(canonical(p) in {canonical(artifact), canonical(pid_file)} for p in (log_path, build_log)):
            raise ValueError('logs must not overwrite the artifact or identity record')
        port = args.port
        parsed = urlsplit(args.health_url)
        loopback = _loopback_host(parsed.hostname)
        diagnostic_host = loopback or '127.0.0.1'
        if port is None and loopback:
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        record = read_record(pid_file, project)
        old = None
        try:
            if record is not None:
                old = OwnedProcess(record['pid'])
                old.verify(record, project)
                if port_occupied(port, diagnostic_host) and (record.get('local_port'), record.get('local_host')) != (port, diagnostic_host):
                    raise ValueError('requested port is occupied outside the recorded service port; existing service retained')
            elif port_occupied(port, diagnostic_host):
                raise ValueError('port is occupied without a matching owned record; no process stopped')
            excluded = (pid_file, log_path, build_log)
            fresh, reason = artifact_fresh(artifact, project, excluded)
            if args.skip_build and not fresh:
                raise ValueError('skip-build refused: ' + reason)
            with log_path.open('ab') as output, build_log.open('ab') as build_output:
                if build is not None:
                    log('building; output remains in the build log')
                    completed = subprocess.run(build, cwd=project, env=env, shell=False,
                                               stdin=subprocess.DEVNULL, stdout=build_output,
                                               stderr=subprocess.STDOUT, timeout=args.build_timeout,
                                               **_launch_options())
                    if completed.returncode:
                        raise ValueError('build failed; existing owned service was not stopped')
                    fresh, reason = artifact_fresh(artifact, project, excluded)
                    if not fresh:
                        raise ValueError('build did not produce a current artifact; existing service retained: ' + reason)
                if old is not None:
                    old.verify(record, project)
                    old.stop()
                    local_child = _CHILDREN.pop(record['pid'], None)
                    if local_child is not None:
                        local_child.wait(timeout=6)
                    remove_record(pid_file, record)
                    log('previous owned instance stopped after successful build validation')
                deadline = time.monotonic() + 3
                while port_occupied(port, diagnostic_host) and time.monotonic() < deadline:
                    time.sleep(0.1)
                if port_occupied(port, diagnostic_host):
                    raise ValueError('port remains occupied; no other listener will be stopped')
                proc, process, new_record = None, None, None
                try:
                    proc = subprocess.Popen(start, cwd=project, env=env, shell=False,
                                            stdin=subprocess.DEVNULL, stdout=output,
                                            stderr=subprocess.STDOUT, close_fds=True,
                                            **_launch_options())
                    process = OwnedProcess(proc.pid)
                    new_record = process.record(project, start[0])
                    new_record['local_port'] = port
                    new_record['local_host'] = diagnostic_host
                    write_record(pid_file, new_record)
                    if not wait_ready(args.health_url, args.timeout, args.allow_remote, process):
                        raise ValueError('new service exited or readiness timed out')
                    _CHILDREN[proc.pid] = proc
                    log('service ready; managed identity record saved')
                    return 0
                except (Exception, KeyboardInterrupt):
                    try:
                        _cleanup_new(proc, process)
                        if new_record is not None:
                            remove_record(pid_file, new_record)
                        log('newly launched process cleaned up; logs were not displayed')
                    except (OSError, ValueError, subprocess.TimeoutExpired):
                        log('cleanup failed; retain the identity record and inspect the owned instance')
                        raise RuntimeError('new process cleanup incomplete') from None
                    raise
                finally:
                    if process is not None:
                        process.close()
        finally:
            if old is not None:
                old.close()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project-dir', required=True)
    p.add_argument('--artifact')
    builds = p.add_mutually_exclusive_group()
    builds.add_argument('--build-cmd', help='legacy command text; no shell interpretation')
    builds.add_argument('--build-argv', help='JSON string array, recommended for paths/arguments')
    starts = p.add_mutually_exclusive_group()
    starts.add_argument('--start-cmd', help='foreground executable command; no shell interpretation')
    starts.add_argument('--start-argv', help='JSON string array for a foreground service')
    p.add_argument('--health-url')
    p.add_argument('--allow-remote', action='store_true')
    p.add_argument('--port', type=int, help='local occupancy diagnostic only; never kills by port')
    p.add_argument('--pid-file', help='managed JSON identity record; integer PID files are refused')
    p.add_argument('--stop', action='store_true', help='stop only the matching recorded owned process')
    p.add_argument('--timeout', type=float, default=120)
    p.add_argument('--build-timeout', type=float, default=300)
    p.add_argument('--skip-build', action='store_true')
    p.add_argument('--log-file')
    p.add_argument('--build-log-file')
    p.add_argument('--pass-env', action='append', default=[], metavar='NAME', help='explicitly pass one named environment variable; repeat as needed')
    args = p.parse_args(argv)
    try:
        return execute(args)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, KeyboardInterrupt) as exc:
        if isinstance(exc, subprocess.SubprocessError):
            log('failed: build/start subprocess did not complete; logs retained locally')
        elif isinstance(exc, KeyboardInterrupt):
            log('interrupted; completed cleanup of any newly managed process')
        else:
            log('failed: ' + str(exc))
        return 1


if __name__ == '__main__':
    sys.exit(main())
