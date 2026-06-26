#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_init_patch.py — 基于扫描结果生成 SDK 接入方案

输入：
  detect_framework.py 的结果 JSON + scan_integration_points.py 的结果 JSON
  + 用户提供的接入参数（user_action_set_id / secret_key / appid 等）

输出：
  结构化的接入方案 JSON，包含：
    - 前置工作（分发开关 / 安全域名 / 权限声明等）
    - 依赖安装命令
    - 文件改动方案：按文件列出 { file, action, target_anchor, code_snippet }
    - 手动补埋点清单（自动采集未覆盖的关键行为）
    - 验证步骤

该脚本不执行任何文件写入。它只生成"方案"。
由上层 IDE Agent（CodeBuddy / Cursor / Claude Code）读取方案并调用自身的
edit 工具实施改动，同时保留给用户审阅和 approve 的机会。

使用方式：
  python3 generate_init_patch.py \
    --detect-json detect.json \
    --scan-json scan.json \
    --user-action-set-id 123456 \
    --secret-key YOUR_KEY \
    --appid wx1234567890abcdef
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ─────────────────────────────────────────────────────────
# 各端代码模板（基于 references/ 中的接入流程抽取）
# ─────────────────────────────────────────────────────────

MINI_GAME_INIT_TEMPLATE = """\
// ===== DataNexus 小游戏 SDK 初始化（自动生成，请勿手动修改标记） =====
import {{ SDK }} from '@dn-sdk/minigame';

const dnSdk = new SDK({{
  user_action_set_id: {user_action_set_id},
  secret_key: '{secret_key}',
  appid: '{appid}',
  auto_track: true, // 默认开启：自动采集 TICKET / START_APP / ENTER_FG / ENTER_BG / LOGIN / SHARE / START_PAY / FINISH_PAY / ADD_TO_WISHLIST / CREATE_GAME_ROOM
}});

// === 登录态 + REGISTER / RE_ACTIVE 接入 ===
//
// ⚠️ 数据正确性红线：
//    isNew（是否新注册）和 isReActive（是否沉默回流）**必须由服务端判断后告知客户端**。
//    严禁在客户端用 wx.storage 自判"上次启动时间"或"是否首次启动"——
//    用户清缓存/换机/多设备会导致同一 openid 被反复算成新注册，
//    污染数据源、严重干扰广告归因模型训练。
//
wx.login({{
  success: (res) => {{
    wx.request({{
      url: 'YOUR_SERVER_LOGIN_ENDPOINT',
      data: {{ code: res.code }},
      success: (r) => {{
        const data = r.data || {{}};
        if (!data.openid) return;
        // 1. 设置 openid（必须，否则 SDK 暂停上传）
        dnSdk.setOpenId(data.openid);
        if (data.unionid) dnSdk.setUnionId(data.unionid);
        // 2. 按服务端字段分流上报（一个用户一次登录中只可能命中其中之一）
        if (data.isNew) {{
          dnSdk.onRegister();                                            // 新用户注册
        }} else if (data.isReActive) {{
          dnSdk.track('RE_ACTIVE', {{ backFlowDay: data.backFlowDay ?? 30 }}); // 沉默回流
        }}
      }},
    }});
  }},
}});
// ===== DataNexus SDK 初始化结束 =====
"""

# Cocos Creator 3.x 小游戏专用模板（import 放文件顶，init 调用放 onLoad）
MINI_GAME_INIT_TEMPLATE_COCOS = {
    "import_statement": "import {{ SDK as DataNexusSDK }} from '@dn-sdk/minigame';",
    "class_private_method": """
    private dnSdk: any = null;
    /** RE_ACTIVE 沉默回流统一档位（30 天，由服务端按此判断后告知客户端） */
    private readonly DN_RE_ACTIVE_DAYS = 30;

    /**
     * 初始化 DataNexus SDK（自动生成，请勿手动修改）
     * 必须先于其他 wx.* 调用初始化，确保启动链路完整被采集
     */
    private initDataNexusSDK() {{
        this.dnSdk = new DataNexusSDK({{
            user_action_set_id: {user_action_set_id},
            secret_key: '{secret_key}',
            appid: '{appid}',
            auto_track: true, // 自动采集 START_APP / ENTER_FG / ENTER_BG / SHARE 等
        }});
        // 上报"完成加载"（IAA 小游戏必报事件）
        try {{
            this.dnSdk.track?.('LOAD_FINISH');
        }} catch (e) {{ /* ignore */ }}

        // === REGISTER / RE_ACTIVE 接入（请按下方 TODO 实现）===
        //
        // ⚠️ 数据正确性红线：
        //    REGISTER（是否新用户）和 RE_ACTIVE（是否沉默回流）**必须由服务端判断**。
        //    严禁客户端用 wx.storage 自判"上次启动时间"做对比 ——
        //    用户清缓存/换机会让同一 openid 被反复算成"新注册"，
        //    污染数据源、干扰广告归因模型训练。
        //
        // 正确接入步骤：
        //    1) wx.login → 用 res.code 调你的业务后端
        //    2) 后端用 code 换 openid → 查 DB 判断 isNew / isReActive，并返回：
        //         {{ openid, isNew, isReActive, backFlowDay }}
        //    3) 客户端按字段分流上报：
        //
        // wx.login({{
        //   success: (res) => {{
        //     wx.request({{
        //       url: 'YOUR_BIZ_LOGIN_API',
        //       method: 'POST',
        //       data: {{ code: res.code }},
        //       success: ({{ data }}) => {{
        //         this.dnSdk.setOpenId?.(data.openid);
        //         if (data.isNew) {{
        //           this.dnSdk.onRegister?.();          // 新用户注册
        //         }} else if (data.isReActive) {{
        //           this.dnSdk.track?.('RE_ACTIVE', {{ // 沉默回流
        //             backFlowDay: data.backFlowDay ?? this.DN_RE_ACTIVE_DAYS,
        //           }});
        //         }}
        //       }},
        //     }});
        //   }},
        // }});
    }}
""",
    "onload_call": "        // 必须在 WechatGameTool.init() 之前：DataNexus SDK 接管 wx.* 上报\\n        this.initDataNexusSDK();",
}

MINI_PROGRAM_INIT_TEMPLATE = """\
// ===== DataNexus 小程序 SDK 初始化（自动生成） =====
import {{ SDK }} from '@dn-sdk/miniprogram';

const dnSdk = new SDK({{
  user_action_set_id: {user_action_set_id},
  secret_key: '{secret_key}',
  appid: '{appid}',
  auto_track: true,
}});

// === 登录态 + REGISTER / RE_ACTIVE 接入 ===
//
// ⚠️ 数据正确性红线：
//    isNew / isReActive **必须由服务端判断**，严禁客户端用 wx.storage 自判，
//    否则用户清缓存/换机/多设备会污染数据源。
//
wx.login({{
  success: (res) => {{
    wx.request({{
      url: 'YOUR_SERVER_LOGIN_ENDPOINT',
      data: {{ code: res.code }},
      success: (r) => {{
        const data = r.data || {{}};
        if (!data.openid) return;
        dnSdk.setOpenId(data.openid);
        if (data.unionid) dnSdk.setUnionId(data.unionid);
        if (data.isNew) {{
          dnSdk.onRegister();
        }} else if (data.isReActive) {{
          dnSdk.track('RE_ACTIVE', {{ backFlowDay: data.backFlowDay ?? 30 }});
        }}
      }},
    }});
  }},
}});
// ===== DataNexus SDK 初始化结束 =====
"""

ANDROID_INIT_TEMPLATE_JAVA = """\
// ===== DataNexus Android SDK 初始化（自动生成） =====
import com.qq.gdt.action.GDTAction;

// ⚠️ 建议在 Application.onCreate() 中调用：
// public class MyApplication extends Application {{
//     @Override
//     public void onCreate() {{
//         super.onCreate();
        GDTAction.init(this, "{user_action_set_id}", "{secret_key}");
        GDTAction.start(); // v2.1+ 必须调用，否则 SDK 不工作
//     }}
// }}
// ===== DataNexus SDK 初始化结束 =====
"""

ANDROID_INIT_TEMPLATE_KOTLIN = """\
// ===== DataNexus Android SDK 初始化（自动生成） =====
import com.qq.gdt.action.GDTAction

// ⚠️ 建议在 Application.onCreate() 中调用：
// class MyApplication : Application() {{
//     override fun onCreate() {{
//         super.onCreate()
        GDTAction.init(this, "{user_action_set_id}", "{secret_key}")
        GDTAction.start()
//     }}
// }}
// ===== DataNexus SDK 初始化结束 =====
"""

IOS_INIT_TEMPLATE_OBJC = """\
// ===== DataNexus iOS SDK 初始化（自动生成） =====
#import <GDTActionSDK/GDTAction.h>
#import <GDTActionSDK/GDTAction+convenience.h>

// 请放在 AppDelegate 的 didFinishLaunchingWithOptions 内：
// - (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {{
    [GDTAction init:@"{user_action_set_id}" secretKey:@"{secret_key}"];
    [GDTAction start]; // v2.1+ 必须调用
// }}

// 另请在 applicationDidBecomeActive 中手动上报 START_APP：
// - (void)applicationDidBecomeActive:(UIApplication *)application {{
//     [GDTAction logAction:@"START_APP" actionParam:nil];
// }}
// ===== DataNexus SDK 初始化结束 =====
"""

IOS_INIT_TEMPLATE_SWIFT = """\
// ===== DataNexus iOS SDK 初始化（自动生成） =====
import GDTActionSDK

// 请放在 AppDelegate.application(_:didFinishLaunchingWithOptions:) 内：
GDTAction.init("{user_action_set_id}", secretKey: "{secret_key}")
GDTAction.start()

// 并在 applicationDidBecomeActive 中手动上报 START_APP：
// GDTAction.logAction("START_APP", actionParam: nil)
// ===== DataNexus SDK 初始化结束 =====
"""

HARMONY_INIT_TEMPLATE = """\
// ===== DataNexus 鸿蒙 SDK 初始化（自动生成） =====
import dnSDK from '@dn-sdk/harmony';
import { AbilityConstant, Want } from '@kit.AbilityKit';

// 请放在 EntryAbility.onCreate 内：
// onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {{
    dnSDK.init({
        context: this.context,
        user_action_set_id: {user_action_set_id},
        secret_key: '{secret_key}',
        // 可选：show_log: true,  // 开启调试日志
    });
    dnSDK.start();
// }}
// ===== DataNexus SDK 初始化结束 =====
"""


# ─────────────────────────────────────────────────────────
# 前置工作说明（每端差异）
# ─────────────────────────────────────────────────────────

PREREQUISITE_INSTRUCTIONS = {
    "mini-game": [
        "📋 前置工作（必须完成）：",
        "  1. DataNexus 平台创建专用数据源（建议新建），获取 user_action_set_id 与 secret_key",
        "  2. 数据源绑定对应小游戏 AppID",
        "  3. 分发开关：开启「一方数据合作」「转化归因」",
        "  4. 在微信公众平台 → 开发设置 → 服务器域名中添加 request 合法域名：",
        "     https://api.datanexus.qq.com",
        "  5. 申请微信 AppID 关联：DataNexus 平台 → 数据接入 → 工具箱 → 申请微信 AppID（管理员 2 工作日内审批）",
        "  6. IAA 小游戏（广告变现）需额外填写接入申请表",
    ],
    "mini-program": [
        "📋 前置工作（必须完成）：",
        "  1. DataNexus 平台创建专用数据源，获取 user_action_set_id 与 secret_key",
        "  2. 数据源绑定对应小程序 AppID",
        "  3. 分发开关：开启「一方数据合作」「转化归因」",
        "  4. 微信公众平台 → 开发 → 开发管理 → 开发设置 → 服务器域名中添加 request 合法域名：",
        "     https://api.datanexus.qq.com",
        "  5. 申请微信 AppID 关联",
    ],
    "android": [
        "📋 前置工作（必须完成）：",
        "  1. DataNexus 平台创建专用数据源，获取 userActionSetId 与 appSecretKey",
        "  2. 分发开关：",
        "     • 游戏类 APP：开启「一方数据合作」「转化归因」",
        "     • 非游戏类 APP：开启「一方数据合作」「预归因」「智能场景匹配」，关闭「转化归因」",
        "  3. 在 AndroidManifest.xml 中添加 INTERNET 权限（必须）及可选的 ACCESS_NETWORK_STATE",
        "  4. 如开启 ProGuard 混淆，需添加规则：-keep class com.qq.gdt.action.** { *; }",
        "  5. 建议集成 OAID SDK 2.8.0+ 提升归因",
    ],
    "ios": [
        "📋 前置工作（必须完成）：",
        "  1. DataNexus 平台创建专用数据源，获取 actionSetId 与 secretKey",
        "  2. 分发开关：开启「一方数据合作」「预归因」「智能场景匹配」，关闭「转化归因」",
        "  3. CocoaPods 集成：Podfile 中添加 pod 'GDTActionSDK' 后执行 pod install",
        "  4. 手动集成需在 Build Settings → Other Linker Flags 中添加 -ObjC",
        "  5. 依赖库：AdSupport.framework / CoreTelephony.framework / SystemConfiguration.framework",
    ],
    "harmony": [
        "📋 前置工作（必须完成）：",
        "  1. DataNexus 平台创建专用数据源，获取 user_action_set_id 与 secret_key",
        "  2. 分发开关：按 APP 类型配置",
        "  3. 在 module.json5 中声明权限：ohos.permission.INTERNET / ohos.permission.GET_NETWORK_INFO",
        "  4. ohpm 集成：ohpm install @dn-sdk/harmony",
    ],
}

DEPENDENCY_COMMANDS = {
    "mini-game": ["npm i @dn-sdk/minigame"],
    "mini-program": ["npm i @dn-sdk/miniprogram"],
    "android": [
        "# 将 GDTActionSDK.min.x.x.x.aar 放入 app/libs/",
        "# 在 app/build.gradle 的 dependencies 中添加：",
        "# implementation(name: 'GDTActionSDK.min.x.x.x', ext: 'aar')",
    ],
    "ios": ["pod 'GDTActionSDK'", "pod install"],
    "harmony": ["ohpm install @dn-sdk/harmony"],
}

POST_INTEGRATION_MANUAL_EVENTS = {
    "mini-game": [
        "RE_ACTIVE（沉默唤起，老用户回归；单档位触发，默认 backFlowDay=30）",
        "LOAD_FINISH（loading 页完成）",
        "SUBSCRIBE（订阅成功）",
        "PURCHASE（付费，必须传 value，单位：分）",
        "CREATE_ROLE / TUTORIAL_START / TUTORIAL_FINISH / UPDATE_LEVEL（如有）",
    ],
    "mini-program": [
        "REGISTER（新用户首次打开）",
        "PURCHASE（付费，必须传 value，单位：分）",
        "行业特定事件（短剧：SELECT_RECHARGE_LEVEL；电商：PRODUCT_VIEW / ADD_TO_CART / COMPLETE_ORDER）",
    ],
    "android": [
        "START_APP（Android v1.9.4+ 默认自动采集，如关闭了自动采集才需手动冷启+热启各一次）",
        "REGISTER / LOGIN",
        "PURCHASE（必须传 value）",
        "CREATE_ROLE / TUTORIAL_FINISH（游戏类）",
    ],
    "ios": [
        "START_APP（iOS 端不自动采集，需在 applicationDidBecomeActive 手动上报）",
        "REGISTER / LOGIN",
        "PURCHASE（必须传 value）",
    ],
    "harmony": [
        "REGISTER / LOGIN",
        "PURCHASE（必须传 value）",
        "START_APP（鸿蒙端自动采集，不要手动上报）",
    ],
}


# ─────────────────────────────────────────────────────────
# 方案生成
# ─────────────────────────────────────────────────────────

def _pick_init_anchor(scan: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """从扫描结果中挑选最佳 init 插入点"""
    init_points: List[Dict[str, Any]] = scan.get("init_points") or []
    if not init_points:
        return None
    return init_points[0]  # 已按优先级排序


def _pick_init_template(sdk_end: str, details: Dict[str, Any]):
    """
    返回：
      - 传统模板场景：返回字符串（单块代码，Agent 插入到 onLaunch 内）
      - Cocos Creator 场景：返回 dict，含 import_statement / class_private_method / onload_call 三段，
        Agent 需分别写入到"文件顶 / 类内 / onLoad 内"
    """
    lang = (details or {}).get("language", "")
    framework = (details or {}).get("framework", "")
    if sdk_end == "mini-game":
        if framework == "Cocos Creator":
            return MINI_GAME_INIT_TEMPLATE_COCOS
        return MINI_GAME_INIT_TEMPLATE
    if sdk_end == "mini-program":
        return MINI_PROGRAM_INIT_TEMPLATE
    if sdk_end == "android":
        return ANDROID_INIT_TEMPLATE_KOTLIN if "Kotlin" in lang else ANDROID_INIT_TEMPLATE_JAVA
    if sdk_end == "ios":
        return IOS_INIT_TEMPLATE_SWIFT if "Swift" in lang else IOS_INIT_TEMPLATE_OBJC
    if sdk_end == "harmony":
        return HARMONY_INIT_TEMPLATE
    return ""


def generate(
    detect: Dict[str, Any],
    scan: Dict[str, Any],
    user_action_set_id: str,
    secret_key: str,
    appid: Optional[str] = None,
) -> Dict[str, Any]:
    sdk_end = detect.get("sdk_end")
    details = detect.get("details", {}) or {}
    if sdk_end == "unknown" or sdk_end not in RULES_SUPPORTED_SDKS:
        return {
            "success": False,
            "error": f"未知或不支持的 SDK 端：{sdk_end}",
            "fallback": "请走 SKILL.md 能力2（接入开发指引），手动复制代码示例。",
        }

    if not detect.get("auto_integration_supported"):
        return {
            "success": False,
            "error": "当前项目技术栈不在自动化接入白名单",
            "reason": detect.get("auto_integration_reason"),
            "fallback": "请走 SKILL.md 能力2（接入开发指引），手动复制代码示例。",
        }

    # ───── 已接入检测（硬拒绝）─────
    # 区分"真正在用"（new SDK({...}) 已存在）vs "只是装了依赖"（仅 import/require）
    existing_raw = scan.get("existing_sdks") or []
    existing_instantiated = [
        e for e in existing_raw
        if "实例化已存在" in e.get("description", "")
    ]
    existing_imports_only = [
        e for e in existing_raw
        if ("import" in e.get("description", "") or "require" in e.get("description", ""))
        and "实例化" not in e.get("description", "")
    ]

    if existing_instantiated:
        # 硬拒绝：代码里已经在用，重复接入会导致双重上报/内存浪费
        # 基于 scan 结果推断体检场景，避免用户拿到不带 scenario 的错误命令
        scenario_hint = _infer_audit_scenario(sdk_end, scan)
        audit_cmd = (
            f"python3 scripts/audit_integration.py {detect.get('project_root', '<project>')} "
            f"--sdk-end {sdk_end}"
        )
        if scenario_hint:
            audit_cmd += f" --scenario {scenario_hint}"
        else:
            audit_cmd += " --scenario <请根据业务选择：见 audit 脚本 --help>"

        return {
            "success": False,
            "error": "检测到项目中已完成 DataNexus SDK 接入（存在 new SDK({...}) 调用），拒绝重复接入",
            "reason": "重复接入会导致双重事件上报、内存浪费、行为错乱",
            "existing_integration_sites": [
                {
                    "file": e["file"],
                    "line": e["line"],
                    "description": e["description"],
                    "matched_text": e.get("matched_text", ""),
                }
                for e in existing_instantiated[:5]
            ],
            "recommended_action": (
                "【优先推荐】跑 audit_integration.py 做接入质量体检，查看必报事件覆盖率/用法规范/合规问题：\n"
                f"  {audit_cmd}\n"
                "\n其他选项："
                "\n  · 升级/调整现有接入：走 SKILL.md 能力2（接入开发指引）人工修改现有代码"
                "\n  · 排查现有接入问题：走能力6（问题排查）"
                "\n  · 确实想重新接入：请先人工删除现有接入代码（new SDK 调用 + 对应的工具类），再重新执行能力7"
            ),
            "next_action_hint": {
                "command": audit_cmd,
                "scenario_inferred": scenario_hint,
                "description": "推荐的下一步：跑接入体检，查看 SDK 接入质量（必报事件覆盖/用法规范/合规）",
            },
        }
    # ───── 已接入检测结束 ─────

    init_anchor = _pick_init_anchor(scan)

    template = _pick_init_template(sdk_end, details)
    if not template:
        return {
            "success": False,
            "error": f"未找到 {sdk_end} / {details.get('language')} 的代码模板",
        }

    # 两种模板形态：字符串（单块插入）、dict（Cocos Creator 多段插入）
    is_structured = isinstance(template, dict)

    if is_structured:
        code_snippet = None
        structured_snippet = {
            "import_statement": template["import_statement"],
            "class_private_method": template["class_private_method"].format(
                user_action_set_id=user_action_set_id,
                secret_key=secret_key,
                appid=appid or "YOUR_APPID",
            ),
            "onload_call": template["onload_call"],
        }
    else:
        code_snippet = template.format(
            user_action_set_id=user_action_set_id,
            secret_key=secret_key,
            appid=appid or "YOUR_APPID",
        )
        structured_snippet = None

    existing = scan.get("existing_sdks") or []
    event_hooks = scan.get("event_hooks") or []

    # 文件级改动建议
    file_changes: List[Dict[str, Any]] = []
    if init_anchor:
        change: Dict[str, Any] = {
            "file": init_anchor["file"],
            "action": "insert_at_anchor",
            "anchor_line": init_anchor["line"],
            "anchor_description": init_anchor["description"],
            "anchor_matched_text": init_anchor["matched_text"],
        }
        if is_structured:
            change["insertion_rule"] = (
                "Cocos Creator 3.x 三段插入："
                "(a) import_statement 加到文件顶部（现有 import 之后）；"
                "(b) class_private_method 作为新方法加到组件类内（建议放在 onLoad 之前）；"
                "(c) onload_call 插入到 onLoad() 方法体第一行（在其他业务初始化之前）"
            )
            change["structured_snippet"] = structured_snippet
        else:
            change["insertion_rule"] = "将下方 code_snippet 插入到 anchor 所在生命周期方法内的第一行（在 super 调用之后，其他业务逻辑之前）"
            change["code_snippet"] = code_snippet
        file_changes.append(change)
    else:
        # 没扫到入口 → 给降级方案
        fallback_change: Dict[str, Any] = {
            "file": "<需用户指定>",
            "action": "manual",
            "insertion_rule": "未扫到生命周期入口，建议用户指定 Application/AppDelegate/EntryAbility 所在文件后再继续",
        }
        if is_structured:
            fallback_change["structured_snippet"] = structured_snippet
        else:
            fallback_change["code_snippet"] = code_snippet
        file_changes.append(fallback_change)

    plan: Dict[str, Any] = {
        "success": True,
        "sdk_end": sdk_end,
        "summary": {
            "project_root": detect.get("project_root"),
            "framework": details.get("framework"),
            "language": details.get("language"),
            "package_manager": details.get("package_manager"),
            "auto_integration_supported": True,
        },
        "step_1_prerequisites": PREREQUISITE_INSTRUCTIONS.get(sdk_end, []),
        "step_2_install_dependencies": DEPENDENCY_COMMANDS.get(sdk_end, []),
        "step_3_code_changes": file_changes,
        "step_4_manual_events_to_track": POST_INTEGRATION_MANUAL_EVENTS.get(sdk_end, []),
        "step_5_validation": [
            "完成代码改动后，运行：python3 scripts/validate_integration.py <project_root> --sdk-end {}".format(sdk_end),
            "真机/模拟器运行 → 查看控制台日志 TAG（gdt_action 或 @dn-sdk/*）确认 init 成功",
            "DataNexus 平台 → 日志查询 → 输入 user_action_set_id 验证数据到达",
        ],
        "warnings": [],
    }

    # 冲突警告
    # 注意：到这里说明没有"实例化"命中（否则上面已经硬拒绝返回），
    # 这里处理的是"只 import 没用"或"有友商 SDK"的情况
    if existing_imports_only:
        plan["warnings"].append({
            "type": "sdk_dependency_installed_but_unused",
            "count": len(existing_imports_only),
            "severity": "info",
            "message": "检测到 DataNexus SDK 依赖已安装（package.json 里有 @dn-sdk/minigame），"
                       "但代码中未发现实例化调用。这是典型的'依赖已装但未接入'状态，本次接入将补齐实例化代码。",
            "details": [{"file": e["file"], "line": e["line"], "desc": e["description"]} for e in existing_imports_only[:5]],
        })
    else:
        # 二次检测：代码里没 import，但 package.json 可能已装依赖
        pkg_dep_warning = _check_package_json_unused_dep(detect.get("project_root", ""), sdk_end)
        if pkg_dep_warning:
            plan["warnings"].append(pkg_dep_warning)

    # 过滤出友商 SDK / 旧版 GDT，这些是需要警告的真正"第三方"
    other_sdks = [
        e for e in existing
        if "DataNexus" not in e.get("description", "")
        and "实例化" not in e.get("description", "")
    ]
    if other_sdks:
        plan["warnings"].append({
            "type": "third_party_sdk_detected",
            "count": len(other_sdks),
            "severity": "warn",
            "message": "检测到项目中已存在其他归因 SDK（非 DataNexus），接入前请评估是否需要迁移或并存",
            "details": [{"file": e["file"], "line": e["line"], "desc": e["description"]} for e in other_sdks[:10]],
        })

    # 如果找到的 init 入口太多（>5），给出多入口提示
    init_points = scan.get("init_points") or []
    if len(init_points) > 5:
        plan["warnings"].append({
            "type": "multiple_init_candidates",
            "count": len(init_points),
            "message": f"项目中发现 {len(init_points)} 个可能的 init 插入点，建议人工确认选中的 anchor 是否正确（见 step_3 第一个改动点）",
        })

    # 告诉 Agent 自动采集能覆盖多少业务事件
    if event_hooks:
        plan["auto_track_coverage_hint"] = {
            "count": len(event_hooks),
            "message": f"SDK 开启 auto_track 后，可自动采集 {len(event_hooks)} 个业务事件点（无需手动埋点）",
            "covered_events_sample": [e["description"] for e in event_hooks[:5]],
        }

    return plan


RULES_SUPPORTED_SDKS = {"mini-game", "mini-program", "android", "ios", "harmony"}


def _infer_audit_scenario(sdk_end: str, scan: Dict[str, Any]) -> Optional[str]:
    """
    基于 scan 结果推断体检场景，用于硬拒绝时给用户一个带 --scenario 的可直接跑的命令。

    推断依据（保守策略：只在有强信号时返回，不确定就返回 None 让用户显式选）：
      - mini-game：扫到 wx.requestPayment → iap-mini-game；扫到激励视频/Banner → iaa-mini-game
      - mini-program：扫到 requestPayment 但无行业特征 → general-mini-program
      - android / ios：有付费 SDK（微信支付/支付宝）→ game-app（保守猜）；否则 general-app
      - harmony：只支持 general-app，直接返回
    """
    event_hooks: List[Dict[str, Any]] = scan.get("event_hooks") or []
    descs = " | ".join(h.get("description", "") for h in event_hooks).lower()

    if sdk_end == "harmony":
        return "general-app"

    if sdk_end == "mini-game":
        has_payment = "付费" in descs or "purchase" in descs or "requestpayment" in descs
        has_ad = "广告" in descs or "iaa" in descs or "激励视频" in descs
        if has_payment:
            return "iap-mini-game"
        if has_ad:
            return "iaa-mini-game"
        return None  # 不确定，让用户显式选

    if sdk_end == "mini-program":
        # 无明确行业线索 → 走通用场景
        return "general-mini-program"

    if sdk_end in {"android", "ios"}:
        # 有支付 SDK 的大概率是商业化 APP
        return "general-app"

    return None


# 依赖名映射：用于检查 package.json 里是否已装 DN SDK
SDK_DEP_NAMES = {
    "mini-game": ["@dn-sdk/minigame"],
    "mini-program": ["@dn-sdk/miniprogram"],
    # android / ios / harmony 不通过 package.json 管理依赖
}


def _check_package_json_unused_dep(project_root: str, sdk_end: str) -> Optional[Dict[str, Any]]:
    """
    检查 package.json 里是否已装 DN SDK 依赖，但代码中完全没 import/require。
    这是典型的"依赖已装但未接入"残留状态（比如之前接入后又被手动删除了）。
    """
    if sdk_end not in SDK_DEP_NAMES:
        return None
    try:
        p = Path(project_root) / "package.json"
        if not p.exists():
            return None
        pkg = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        deps = {}
        deps.update(pkg.get("dependencies", {}) or {})
        deps.update(pkg.get("devDependencies", {}) or {})
        matched = [name for name in SDK_DEP_NAMES[sdk_end] if name in deps]
        if not matched:
            return None
        return {
            "type": "sdk_dependency_in_package_json_but_no_code",
            "severity": "info",
            "dependencies": matched,
            "versions": {name: deps[name] for name in matched},
            "message": (
                f"package.json 已声明 {matched[0]} 依赖（版本 {deps[matched[0]]}），"
                f"但代码中未检测到 import/实例化。疑似历史接入残留或未完成的接入，"
                f"本次接入将补齐代码（无需重新 npm i）。"
            ),
        }
    except (OSError, json.JSONDecodeError, KeyError):
        return None


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="生成 SDK 接入方案（patch 预案）")
    parser.add_argument("--detect-json", required=True, help="detect_framework.py 输出的 JSON 文件路径")
    parser.add_argument("--scan-json", required=True, help="scan_integration_points.py 输出的 JSON 文件路径")
    parser.add_argument("--user-action-set-id", required=True, help="数据源 ID")
    parser.add_argument("--secret-key", required=True, help="数据源密钥（注意：不会落盘，仅生成方案文本时替换占位符）")
    parser.add_argument("--appid", default=None, help="应用 AppID（小程序/小游戏必填）")
    parser.add_argument("--output", default=None, help="方案输出路径，不指定则 stdout")
    args = parser.parse_args()

    try:
        with open(args.detect_json, encoding="utf-8") as f:
            detect = json.load(f)
        with open(args.scan_json, encoding="utf-8") as f:
            scan = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"❌ 读取输入失败：{e}", file=sys.stderr)
        return 1

    plan = generate(
        detect=detect,
        scan=scan,
        user_action_set_id=args.user_action_set_id,
        secret_key=args.secret_key,
        appid=args.appid,
    )

    text = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        # 人类可读的简短提示（特别是硬拒绝场景）
        if not plan.get("success"):
            print(f"❌ 方案未生成（硬拒绝）")
            print(f"   原因：{plan.get('error')}")
            if plan.get("reason"):
                print(f"   细节：{plan.get('reason')}")
            if plan.get("existing_integration_sites"):
                print(f"   已接入位置：")
                for site in plan["existing_integration_sites"][:3]:
                    print(f"     · {site['file']}:{site['line']} - {site['description']}")
            if plan.get("recommended_action"):
                print(f"   建议：{plan.get('recommended_action')}")
            print(f"   详细 JSON 已写入：{args.output}")
        else:
            print(f"✅ 方案已写入 {args.output}")
    else:
        print(text)

    return 0 if plan.get("success") else 2


if __name__ == "__main__":
    sys.exit(main())
