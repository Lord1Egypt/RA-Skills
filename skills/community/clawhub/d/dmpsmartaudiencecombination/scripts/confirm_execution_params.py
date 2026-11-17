#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""confirm_execution_params.py - Step 8.5 执行口径确认提示

创建人群组合前，必须向用户确认终端类型(trackType)和设备ID类型(idTypes)。
本脚本输出强制交互提示，防止AI跳过该步骤直接调用创建接口。

用法：
  python3 scripts/confirm_execution_params.py
"""

import sys


PROMPT = """
===STEP9_EXECUTION_PARAMS_PROMPT===
⛔【AI必须先询问用户以下参数，禁止直接创建人群】

在调用create_must_baseline.py/create_combined_crowd.py之前，必须向用户确认以下执行口径参数：

1️⃣ 终端类型（trackType，必选，单选）：
   - MOBILE：移动端（手机端投放，最常用）
   - PC：PC端
   - OTT：OTT大屏端

2️⃣ 设备ID类型（idTypes，必选，可多选）：
   移动端常用：IDFA（iOS）、OAID（安卓）、MD5_IDFA、MD5_OAID、MD5_IMEI
   PC端常用：MZID
   OTT端常用：MD5_MAC
   
   💡 默认推荐：MOBILE + IDFA,OAID,MD5_IDFA,MD5_OAID,MD5_IMEI（覆盖iOS+安卓最广）

3️⃣ 人群名称（name）：自动生成有意义的名称（含需求关键词+日期+组合类型），不需要询问用户

【询问话术模板】：
📋 创建人群前需要确认执行口径：
• 终端类型：默认移动端，需要改吗？
• 设备ID：默认IDFA+OAID+对应MD5（覆盖iOS+安卓），需要调整吗？
回复"确认"使用默认值，或说明需要调整。

⛔ 禁止行为：
- ❌ 未询问用户就直接调用create_must_baseline.py/create_combined_crowd.py
- ❌ 擅自替用户决定idTypes（不得用"全选"或"默认所有"而不告知用户）
- ❌ 跳过本步骤直接进入Step 9创建人群
===END_STEP9_PROMPT===
"""


def main():
    print(PROMPT.strip())
    # 输出默认推荐参数供AI参考
    defaults = {
        "trackType": "MOBILE",
        "idTypes": ["IDFA", "OAID", "MD5_IDFA", "MD5_OAID", "MD5_IMEI"],
        "note": "默认值仅作为推荐参考，必须经用户确认后方可使用"
    }
    import json
    print("\n[DEFAULT_PARAMS]", json.dumps(defaults, ensure_ascii=False))


if __name__ == "__main__":
    main()
