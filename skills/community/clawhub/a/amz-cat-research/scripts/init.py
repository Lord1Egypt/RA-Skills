#!/usr/bin/env python3
"""
init.py — 亚马逊类目调研 Skill 初始化配置检查

功能：
  1. 检查 OpenClaw 浏览器状态
  2. 检查卖家精灵插件是否安装并登录
  3. 检查 SIF 插件是否安装并登录
  4. 生成配置状态报告
  5. 提供修复建议

agent 调用流程:
  1. python3 init.py check      # 生成检查 JS
  2. browser act(kind="evaluate", fn=检查JS)
  3. python3 init.py report '<result_json>'  # 生成配置报告

返回状态:
  - ready: 所有配置就绪，可开始采集
  - partial: 部分配置就绪，某些字段可能无法获取
  - blocked: 配置未就绪，需要用户干预
"""

import sys
import json


def generate_check_js() -> str:
    """生成浏览器插件检查 JS 代码"""
    js = """(() => {
  const result = {
    browser_ready: true,
    page_url: location.href,
    timestamp: new Date().toISOString()
  };

  // 检查卖家精灵插件
  const spiritContainers = [
    '#seller-sprite-extension-quick-view-listing',
    '[id*="seller-sprite"]',
    '[class*="seller-spirit"]',
    '[class*="SellerSpirit"]'
  ];
  
  let spiritFound = false;
  let spiritLoggedIn = false;
  let spiritData = null;
  
  for (const sel of spiritContainers) {
    const el = document.querySelector(sel);
    if (el) {
      spiritFound = true;
      const text = el.innerText || '';
      spiritData = text.substring(0, 500);
      // 检查是否登录（包含商品数据表示已登录）
      if (text.includes('品牌') || text.includes('销量') || text.includes('FBA') || text.includes('上架时间') ||
          text.includes('Brand') || text.includes('Sales') || text.includes('FBA Fee') || text.includes('Listing Date')) {
        spiritLoggedIn = true;
      }
      break;
    }
  }
  
  result.spirit_installed = spiritFound;
  result.spirit_logged_in = spiritLoggedIn;
  result.spirit_data_snippet = spiritData;

  // 检查 SIF 插件
  const sifContainers = [
    '[data-sif-container]',
    '.sif-extension-container',
    '[class*="sif-"]',
    '[class*="SIF"]',
    '[id*="sif"]'
  ];
  
  let sifFound = false;
  let sifLoggedIn = false;
  let sifData = null;
  
  for (const sel of sifContainers) {
    const el = document.querySelector(sel);
    if (el) {
      sifFound = true;
      const text = el.innerText || '';
      sifData = text.substring(0, 300);
      // 检查是否登录
      if (text.includes('流量词') || text.includes('ASIN') || text.includes('广告') ||
          text.includes('Keyword') || text.includes('Traffic') || text.includes('Ad')) {
        sifLoggedIn = true;
      }
      break;
    }
  }
  
  result.sif_installed = sifFound;
  result.sif_logged_in = sifLoggedIn;
  result.sif_data_snippet = sifData;

  // 检查页面是否是亚马逊商品页
  result.is_amazon_page = location.hostname.includes('amazon');
  result.has_asin = /\\/dp\\/[A-Z0-9]{10}/.test(location.pathname);

  return JSON.stringify(result, null, 1);
})()"""
    return js


def generate_report(check_result: dict) -> dict:
    """
    根据浏览器检查结果生成配置状态报告

    输入:
        check_result: dict — 浏览器 evaluate 返回的检查结果，字段包括:
            - browser_ready: bool — 浏览器是否就绪
            - page_url: str — 当前页面 URL
            - spirit_installed: bool — 卖家精灵插件是否安装
            - spirit_logged_in: bool — 卖家精灵是否已登录
            - sif_installed: bool — SIF 插件是否安装
            - sif_logged_in: bool — SIF 是否已登录
            - is_amazon_page: bool — 当前页面是否为亚马逊站点
            - has_asin: bool — 当前页面路径是否包含 ASIN

    输出:
        dict — 配置报告，字段包括:
            - status: str — "ready" | "partial" | "blocked"
            - status_description: str — 状态的中文描述
            - issues: list[str] — 阻断性问题列表
            - warnings: list[str] — 警告列表
            - suggestions: list[str] — 修复建议列表
            - readiness: dict — 各组件就绪状态
            - available_fields: list[str] — 当前配置下可用的采集字段

    条件:
        - check_result 必须是 dict 类型，否则抛出 ValueError
        - status 优先级: blocked > partial > ready（有 issues 则 blocked，有 warnings 则 partial）
    """
    if not isinstance(check_result, dict):
        raise ValueError("check_result 必须是 dict 类型，收到: " + type(check_result).__name__)
    report = {
        "status": "ready",
        "issues": [],
        "warnings": [],
        "suggestions": [],
        "readiness": {
            "browser": check_result.get("browser_ready", False),
            "spirit_plugin": False,
            "spirit_logged_in": False,
            "sif_plugin": False,
            "sif_logged_in": False,
            "is_amazon_page": False,
            "has_asin": False,
        }
    }

    # 检查卖家精灵
    report["readiness"]["is_amazon_page"] = check_result.get("is_amazon_page", False)
    report["readiness"]["has_asin"] = check_result.get("has_asin", False)

    if not check_result.get("browser_ready"):
        report["issues"].append("浏览器未就绪")
        report["suggestions"].append("请确认浏览器已启动并导航到亚马逊页面")

    if not check_result.get("is_amazon_page"):
        report["warnings"].append("当前页面不是亚马逊页面")
        report["suggestions"].append("请导航到亚马逊商品页面后再进行检查")

    if not check_result.get("has_asin"):
        report["warnings"].append("当前页面未检测到 ASIN")
        report["suggestions"].append("请打开亚马逊商品详情页（含 /dp/ 路径）")

    if not check_result.get("spirit_installed"):
        report["issues"].append("卖家精灵插件未安装")
        report["suggestions"].append("请在浏览器中安装卖家精灵浏览器插件")
        report["readiness"]["spirit_plugin"] = False
    else:
        report["readiness"]["spirit_plugin"] = True
        if not check_result.get("spirit_logged_in"):
            report["warnings"].append("卖家精灵插件未登录")
            report["suggestions"].append("请登录卖家精灵账号")
            report["readiness"]["spirit_logged_in"] = False
        else:
            report["readiness"]["spirit_logged_in"] = True

    # 检查 SIF
    if not check_result.get("sif_installed"):
        report["issues"].append("SIF 插件未安装")
        report["suggestions"].append("请在浏览器中安装 SIF 浏览器插件")
        report["readiness"]["sif_plugin"] = False
    else:
        report["readiness"]["sif_plugin"] = True
        if not check_result.get("sif_logged_in"):
            report["warnings"].append("SIF 插件未登录")
            report["suggestions"].append("请登录 SIF 账号")
            report["readiness"]["sif_logged_in"] = False
        else:
            report["readiness"]["sif_logged_in"] = True

    # 确定整体状态
    if report["issues"]:
        report["status"] = "blocked"
    elif report["warnings"]:
        report["status"] = "partial"
    else:
        report["status"] = "ready"

    # 添加状态描述
    status_descriptions = {
        "ready": "所有配置就绪，可以开始采集",
        "partial": "部分插件未登录，部分字段可能无法获取",
        "blocked": "缺少必要插件，请先安装配置"
    }
    report["status_description"] = status_descriptions[report["status"]]

    # 添加可用字段预估
    available_fields = ["ASIN", "标题", "售价", "星级", "Review数量"]
    if report["readiness"]["spirit_plugin"]:
        available_fields.extend(["30天销量", "FBA费", "上架时间", "BSR排名", "品牌"])
    if report["readiness"]["sif_plugin"]:
        available_fields.extend(["流量词数", "广告分析"])
    
    report["available_fields"] = available_fields

    return report


def main():
    if len(sys.argv) < 2:
        print("""用法:
python3 init.py check           # 生成插件检查 JS
python3 init.py report '<json>' # 根据检查结果生成报告
python3 init.py help            # 显示帮助

示例:
  # 生成检查JS（在浏览器中执行）
  python3 init.py check
  
  # 生成配置报告
  python3 init.py report '{"spirit_installed":true, "spirit_logged_in":true, ...}'
""")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "check":
        js = generate_check_js()
        print(js)
    elif mode == "report":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "需要提供检查结果 JSON"}, ensure_ascii=False))
            sys.exit(1)
        try:
            check_result = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print(json.dumps({"error": "无效的 JSON 格式，请检查传入参数"}, ensure_ascii=False))
            sys.exit(1)
        try:
            report = generate_report(check_result)
        except ValueError as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            sys.exit(1)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif mode == "help":
        print(__doc__)
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
