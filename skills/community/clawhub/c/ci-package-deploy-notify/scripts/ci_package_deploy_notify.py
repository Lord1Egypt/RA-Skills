#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from git_flow import (
    load_config,
    resolve_repos,
    resolve_sqa_members,
    send_feishu_deploy_msg,
    trigger_jenkins_job,
    wait_for_job_completion,
)


def parse_args():
    parser = argparse.ArgumentParser(description="触发 Jenkins 打包/部署，并在成功后发送飞书卡片通知")
    parser.add_argument("--repos", nargs="+", required=True, help="config.json 里的仓库名，可一次传多个")
    parser.add_argument("--branch", required=True, help="构建分支/环境，仅支持 dev / test / demo / sit")
    parser.add_argument("--job-type", choices=("ci", "cd"), default="ci", help="ci=只构建，cd=先构建再部署")
    parser.add_argument("--changes", required=True, help="改动说明，用于通知")
    parser.add_argument("--at", default=None, help="指定要 @ 的成员名，多个可逗号分隔")
    parser.add_argument("--initiator-id", default=None, help="本次触发人的 Feishu user_id/open_id")
    parser.add_argument("--initiator-name", default=None, help="本次触发人的展示名，用于兜底显示")
    parser.add_argument("--force-notify", action="store_true", help="忽略 deploy_notify_envs 限制，强制发送通知")
    parser.add_argument("--wait-timeout", type=int, default=1800, help="等待 Jenkins 完成的超时时间（秒）")
    parser.add_argument("--poll-seconds", type=int, default=10, help="轮询 Jenkins 状态间隔（秒）")
    return parser.parse_args()


def validate_branch(branch):
    allowed = {"dev", "test", "demo", "sit"}
    normalized = str(branch or "").strip().lower()
    if normalized not in allowed:
        raise ValueError("当前 skill 只支持 dev / test / demo / sit，不支持 {}".format(branch))
    return normalized


def run_job(cfg, repo_name, job_type, branch, wait_timeout, poll_seconds):
    print("\n[{}] 触发 {}...".format(repo_name, job_type.upper()), end=" ")
    ok, msg, meta = trigger_jenkins_job(cfg, repo_name, job_type, branch=branch)
    meta = meta or {}
    if not ok:
        print("[FAIL] {}".format(msg))
        if meta.get("job_url"):
            print("[INFO] job_url={}".format(meta.get("job_url")))
        return False, msg, meta.get("build_url"), meta
    print("[OK] {}".format(msg))

    queue_url = meta.get("queue_url")
    build_url = meta.get("build_url")
    duplicate_skipped = bool(meta.get("duplicate_skipped"))
    if meta.get("job_url"):
        print("[INFO] job_url={}".format(meta.get("job_url")))
    if meta.get("queue_url"):
        print("[INFO] queue_url={}".format(meta.get("queue_url")))
    if meta.get("build_url"):
        print("[INFO] build_url={}".format(meta.get("build_url")))
    if duplicate_skipped and meta.get("duplicate_kind"):
        print("[INFO] duplicate_kind={}".format(meta.get("duplicate_kind")))

    ok2, msg2, final_build_url = wait_for_job_completion(
        cfg,
        queue_url=queue_url,
        build_url=build_url,
        timeout_seconds=wait_timeout,
        poll_seconds=poll_seconds,
    )
    final_meta = dict(meta)
    final_meta["build_url"] = final_build_url or build_url
    if ok2:
        print("[OK] {} {}".format(msg2, final_build_url or ""))
        return True, msg2, final_build_url, final_meta

    print("[FAIL] {} {}".format(msg2, final_build_url or ""))
    return False, msg2, final_build_url, final_meta


def run_ci_repo(cfg, repo_name, branch, wait_timeout, poll_seconds):
    ci_ok, ci_msg, ci_url, ci_meta = run_job(
        cfg,
        repo_name=repo_name,
        job_type="ci",
        branch=branch,
        wait_timeout=wait_timeout,
        poll_seconds=poll_seconds,
    )
    return {
        "name": repo_name,
        "ok": ci_ok,
        "stage": "ci",
        "message": ci_msg,
        "ci_url": ci_url,
        "job_url": (ci_meta or {}).get("job_url"),
    }


def run_auto_cd_repo(cfg, repo_name, branch, wait_timeout, poll_seconds):
    cd_ok, cd_msg, cd_url, cd_meta = run_job(
        cfg,
        repo_name=repo_name,
        job_type="cd",
        branch=branch,
        wait_timeout=wait_timeout,
        poll_seconds=poll_seconds,
    )
    return {
        "name": repo_name,
        "ok": cd_ok,
        "stage": "deploy",
        "message": cd_msg,
        "ci_url": cd_url,
        "job_url": (cd_meta or {}).get("job_url"),
    }


def main():
    args = parse_args()
    try:
        args.branch = validate_branch(args.branch)
    except Exception as exc:
        print("[ERROR] {}".format(exc), file=sys.stderr)
        return 1

    cfg = load_config()
    repos = resolve_repos(cfg, args.repos)
    if not repos:
        print("[ERROR] 未解析到任何有效仓库", file=sys.stderr)
        return 1

    try:
        sqa_members = resolve_sqa_members(cfg, args.at)
    except Exception as exc:
        print("[ERROR] {}".format(exc), file=sys.stderr)
        return 1

    success = []
    failed = []

    print("[INFO] Branch/Env: {}".format(args.branch))
    print("[INFO] Requested Type: {}".format("CD(AUTO_CD部署)" if args.job_type == "cd" else "CI(仅构建)"))

    cd_mode = str((cfg.get("jenkins") or {}).get("cd_trigger_mode") or "auto_cd_param").strip().lower()

    repo_names = [name for name, _, _ in repos]

    if args.job_type == "ci":
        max_workers = min(len(repos), 8)
        ci_results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(
                    run_ci_repo,
                    cfg,
                    name,
                    args.branch,
                    args.wait_timeout,
                    args.poll_seconds,
                ): name
                for name in repo_names
            }
            for future in as_completed(future_map):
                name = future_map[future]
                try:
                    ci_results[name] = future.result()
                except Exception as exc:
                    ci_results[name] = {
                        "name": name,
                        "ok": False,
                        "stage": "ci",
                        "message": "并行执行异常: {}".format(exc),
                    }
        for name in repo_names:
            result = ci_results.get(name) or {
                "name": name,
                "ok": False,
                "stage": "ci",
                "message": "未拿到执行结果",
            }
            if result.get("ok"):
                success.append(name)
            else:
                failed.append({
                    "name": name,
                    "stage": "ci",
                    "message": result.get("message"),
                    "ci_url": result.get("ci_url"),
                    "job_url": result.get("job_url"),
                })
    elif cd_mode != "separate_job":
        max_workers = min(len(repos), 8)
        cd_results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(
                    run_auto_cd_repo,
                    cfg,
                    name,
                    args.branch,
                    args.wait_timeout,
                    args.poll_seconds,
                ): name
                for name in repo_names
            }
            for future in as_completed(future_map):
                name = future_map[future]
                try:
                    cd_results[name] = future.result()
                except Exception as exc:
                    cd_results[name] = {
                        "name": name,
                        "ok": False,
                        "stage": "deploy",
                        "message": "并行执行异常: {}".format(exc),
                    }
        for name in repo_names:
            result = cd_results.get(name) or {
                "name": name,
                "ok": False,
                "stage": "deploy",
                "message": "未拿到执行结果",
            }
            if result.get("ok"):
                success.append(name)
            else:
                failed.append({
                    "name": name,
                    "stage": result.get("stage") or "deploy",
                    "message": result.get("message"),
                    "ci_url": result.get("ci_url"),
                    "job_url": result.get("job_url"),
                })
    else:
        for name in repo_names:
            ci_url = None
            cd_url = None
            ci_job_url = None
            cd_job_url = None
            ci_ok, ci_msg, ci_url, ci_meta = run_job(
                cfg,
                repo_name=name,
                job_type="ci",
                branch=args.branch,
                wait_timeout=args.wait_timeout,
                poll_seconds=args.poll_seconds,
            )
            ci_job_url = (ci_meta or {}).get("job_url")
            if not ci_ok:
                failed.append({
                    "name": name,
                    "stage": "ci",
                    "message": ci_msg,
                    "ci_url": ci_url,
                    "job_url": ci_job_url,
                })
                continue

            if args.job_type == "cd":
                cd_ok, cd_msg, cd_url, cd_meta = run_job(
                    cfg,
                    repo_name=name,
                    job_type="cd",
                    branch=args.branch,
                    wait_timeout=args.wait_timeout,
                    poll_seconds=args.poll_seconds,
                )
                cd_job_url = (cd_meta or {}).get("job_url")
                if not cd_ok:
                    failed.append({
                        "name": name,
                        "stage": "cd",
                        "message": cd_msg,
                        "ci_url": ci_url,
                        "cd_url": cd_url,
                        "job_url": cd_job_url or ci_job_url,
                    })
                    continue

            success.append(name)

    print("\n=== 汇总 ===")
    print("成功: {}".format(", ".join(success) if success else "无"))
    if failed:
        for item in failed:
            name = item.get("name")
            stage = str(item.get("stage") or "job").upper()
            err = item.get("message")
            print("失败 - {} [{}]: {}".format(name, stage, err))
            if item.get("ci_url"):
                print("  CI链接: {}".format(item.get("ci_url")))
            if item.get("cd_url"):
                print("  CD链接: {}".format(item.get("cd_url")))
            elif item.get("job_url"):
                print("  Job链接: {}".format(item.get("job_url")))

    if not success:
        return 1

    notify_ok, notify_msg = send_feishu_deploy_msg(
        cfg,
        args.branch,
        success,
        args.changes,
        sqa_members,
        initiator_id=args.initiator_id,
        initiator_name=args.initiator_name,
        force=args.force_notify,
        job_type=args.job_type,
    )
    print("[{}] {}".format("OK" if notify_ok else "FAIL", notify_msg))
    return 0 if notify_ok and not failed else (0 if notify_ok and failed == [] else 1)


if __name__ == "__main__":
    raise SystemExit(main())
