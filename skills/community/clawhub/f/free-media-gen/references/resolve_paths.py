#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 free-media-gen 技能所需的 WorkBuddy 关键路径。

目的：让本技能对**任何用户**开箱可用——不论该用户是否重定向过
WORKBUDDY_CONFIG_DIR / CODEBUDDY_CONFIG_DIR。先读取环境变量，取不到则回退到
默认的 ~/.workbuddy。输出一个 JSON 供 agent 或脚本解析，提示信息走 stderr。

解析三处路径：
  1. 配置根 CONFIG_ROOT —— models.json 所在目录（自定义模型注册表，内含各平台 API 密钥）
       优先级：$WORKBUDDY_CONFIG_DIR（目录存在）
               -> $CODEBUDDY_CONFIG_DIR（目录存在）
               -> ~/.workbuddy
  2. 工作区根 WORKSPACE_ROOT —— 生成的图片/视频、审计报告、每日日志的落盘位置
       优先级：--workspace 参数 -> 当前工作目录
  3. 技能目录 SKILL_DIR —— 本技能自带的 scripts / references 所在位置
       优先级：--skill 参数 -> 由本脚本所在位置向上推导

全程**不使用任何作者本机的绝对路径**（例如技能作者自己的配置/工作区目录），以保证可移植性。
"""
import argparse
import json
import os
import sys

DEFAULT_HOME = os.path.expanduser("~/.workbuddy")


def resolve_config_root():
    """返回 (配置根路径, 来源标识)。"""
    for env in ("WORKBUDDY_CONFIG_DIR", "CODEBUDDY_CONFIG_DIR"):
        v = os.environ.get(env, "")
        if v and os.path.isdir(v):
            return os.path.normpath(v), env
    return os.path.normpath(DEFAULT_HOME), "DEFAULT(~/.workbuddy)"


def resolve_workspace_root(override=None):
    """返回 (工作区根路径, 来源标识)。"""
    if override:
        return os.path.normpath(override), "--workspace"
    return os.path.normpath(os.getcwd()), "cwd(agent workspace)"


def resolve_skill_dir(override=None):
    """返回 (技能目录路径, 来源标识)。"""
    if override:
        return os.path.normpath(override), "--skill"
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.dirname(here)), "script(../..)"


def collect(workspace=None, skill=None):
    """返回解析结果字典（只返回，不打印）。"""
    cr, cr_src = resolve_config_root()
    wr, wr_src = resolve_workspace_root(workspace)
    sd, sd_src = resolve_skill_dir(skill)

    models = os.path.join(cr, "models.json")
    mem = os.path.join(wr, ".workbuddy", "memory")
    outputs = os.path.join(wr, "outputs")
    gen_img = os.path.join(wr, "generated-images")

    return {
        "config_root": cr,
        "config_root_source": cr_src,
        "models_json": models,
        "models_json_exists": os.path.isfile(models),
        "workspace_root": wr,
        "workspace_root_source": wr_src,
        "outputs_dir": outputs,
        "generated_images_dir": gen_img,
        "memory_dir": mem,
        "memory_dir_exists": os.path.isdir(mem),
        "skill_dir": sd,
        "skill_dir_source": sd_src,
        "config_json": os.path.join(sd, "config.json"),
        "config_json_exists": os.path.isfile(os.path.join(sd, "config.json")),
    }


def main():
    ap = argparse.ArgumentParser(
        description="解析 free-media-gen 所需的 WorkBuddy 配置根、工作区根与技能目录")
    ap.add_argument("--workspace", default=None,
                    help="指定工作区根目录（不填则用当前工作目录）")
    ap.add_argument("--skill", default=None,
                    help="指定技能目录（不填则由本脚本位置推导）")
    args = ap.parse_args()

    info = collect(args.workspace, args.skill)
    print(json.dumps(info, ensure_ascii=False, indent=2))

    notes = []
    if not info["models_json_exists"]:
        notes.append(
            "警告：在解析出的配置根下未找到 models.json。请确认 "
            "WORKBUDDY_CONFIG_DIR / CODEBUDDY_CONFIG_DIR 是否正确，或直接向用户询问该路径。")
    if not info["config_json_exists"]:
        notes.append(
            "警告：技能目录下未找到 config.json，媒体模型注册表缺失。")
    if not info["memory_dir_exists"]:
        notes.append(
            "提示：工作区下暂无 .workbuddy/memory 目录，写入每日日志时会自动创建。")
    if notes:
        print("\n".join(notes), file=sys.stderr)


if __name__ == "__main__":
    main()
