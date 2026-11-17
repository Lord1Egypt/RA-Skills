import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def stop_child(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.communicate()

def interrupted(_signum, _frame):
    raise KeyboardInterrupt

signal.signal(signal.SIGTERM, interrupted)
parser = argparse.ArgumentParser()
parser.add_argument("--samples", type=int, default=3)
parser.add_argument("--interval", type=float, default=2)
parser.add_argument("--duration", type=float, default=30)
parser.add_argument("--timeout", type=float, default=12)
parser.add_argument("--thermal-config")
parser.add_argument("--hardware-sensors", action="store_true")
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
if (args.samples < 1 or not all(math.isfinite(v) for v in
    (args.interval, args.duration, args.timeout)) or args.interval < 0
    or args.duration <= 0 or args.timeout <= 0):
    parser.error("Use a positive sample count/duration/timeout and a nonnegative interval")
# Last sample starts at (samples-1)*interval; warn early if the duration can
# never admit it, instead of failing silently at the deadline.
needed = (args.samples - 1) * args.interval
if needed >= args.duration:
    if args.interval > 0:
        q = args.duration / args.interval
        max_fit = int(q) if q == int(q) else int(q) + 1   # samples with i*interval < duration
    else:
        max_fit = args.samples
    print(f"WARNING: duration {args.duration}s cannot fit {args.samples} samples at "
          f"{args.interval}s intervals (only {max_fit} start before the deadline); "
          f"reduce --samples or raise --duration", file=sys.stderr)
options = {"hardware_sensors": args.hardware_sensors}
if args.thermal_config:
    config = Path(args.thermal_config).resolve(strict=True)
    options["thermal_provider_config_paths"] = [str(config)]
worker = "import json,sys,fitctl; print(fitctl.collect_state(**json.loads(sys.argv[1])).to_json())"
args.out.mkdir(parents=True, exist_ok=False)
manifest = {"started_at": utc_now(), "samples": [], "requested_samples": args.samples,
            "interval_seconds": args.interval, "duration_seconds": args.duration,
            "sample_timeout_seconds": args.timeout, "interpreter": sys.executable}
ranges = {}
deadline = time.monotonic() + args.duration
try:
    for index in range(args.samples):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            # Log samples the deadline prevented from ever starting, so the
            # manifest answers "what happened to sample N?" without inference.
            for skipped in range(index, args.samples):
                manifest["samples"].append({"index": skipped, "status": "skipped",
                                            "reason": "overall deadline reached"})
            break
        started = time.monotonic()
        entry = {"index": index, "started_at": utc_now()}
        proc = None
        try:
            proc = subprocess.Popen([sys.executable, "-B", "-c", worker, json.dumps(options)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, start_new_session=True)
            stdout, stderr = proc.communicate(timeout=min(args.timeout, remaining))
            entry.update(returncode=proc.returncode, stderr=stderr[-4096:])
            if proc.returncode:
                entry["status"] = "error"
            else:
                artifact = json.loads(stdout)
                if (artifact["envelope"]["schema_id"] != "host-state.v2"
                    or artifact["state"]["collection_mode"] != "live"):
                    raise ValueError("Expected a live host-state.v2 artifact")
                filename = f"sample-{index:04d}.state.json"
                (args.out / filename).write_text(stdout, encoding="utf-8")
                entry.update(status="collected", artifact=filename)
                thermal = artifact["state"]["core_state"].get("thermal_resources") or {}
                providers = {p["provider_id"]: p["outcome"]
                             for p in thermal.get("providers", [])}
                entry["thermal_provider_outcomes"] = providers
                for reading in thermal.get("readings", []):
                    outcome = providers.get(reading["provider_id"])
                    if (outcome not in ("success", "partial") or
                        reading["status"] not in ("ok", "warning", "critical")):
                        continue
                    identity = {key: reading[key] for key in
                                ("provider_id", "sensor_id", "evidence_target")}
                    key = json.dumps(identity, sort_keys=True)
                    group = ranges.setdefault(key, dict(identity, values_mc=[],
                        observed_first=reading["observed_at"], partial_samples=0,
                        warning_samples=0, critical_samples=0))
                    group["values_mc"].append(reading["temperature_millidegrees_celsius"])
                    group["observed_last"] = reading["observed_at"]
                    group["partial_samples"] += int(outcome == "partial")
                    group["warning_samples"] += int(reading["status"] == "warning")
                    group["critical_samples"] += int(reading["status"] == "critical")
        except subprocess.TimeoutExpired:
            stop_child(proc)
            entry["status"] = "timeout"
        except KeyboardInterrupt:
            if proc is not None:
                stop_child(proc)
            entry["status"] = "interrupted"
            raise
        except (OSError, ValueError, KeyError, TypeError) as error:
            if proc is not None and proc.poll() is None:
                stop_child(proc)
            entry.update(status="error", error=str(error))
        finally:
            entry.update(ended_at=utc_now(), elapsed_seconds=time.monotonic() - started)
            manifest["samples"].append(entry)
        if index + 1 < args.samples:
            time.sleep(max(0, min(args.interval - (time.monotonic() - started),
                                 deadline - time.monotonic())))
finally:
    manifest["ended_at"] = utc_now()
    manifest["sampled_temperature_ranges"] = []
    for group in ranges.values():
        values = group.pop("values_mc")
        group.update(unit="degrees_celsius", valid_sample_count=len(values),
                     minimum=min(values) / 1000, maximum=max(values) / 1000,
                     mean=sum(values) / len(values) / 1000)
        manifest["sampled_temperature_ranges"].append(group)
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(args.out / "manifest.json")
sys.exit(0 if len(manifest["samples"]) == args.samples and
         all(item["status"] == "collected" for item in manifest["samples"]) else 1)
