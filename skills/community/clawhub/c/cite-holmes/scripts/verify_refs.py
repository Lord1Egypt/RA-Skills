"""verify_refs.py — cite-holmes skill 的引用机械验证器。

对研究引用清单做机器可判定的检查（可达性 / 域名权威度 / 字段完整性 / 去重），
输出五态判定报告（Markdown + JSON）。语义验证（来源是否真的支持论断）由模型
在研究流程中完成，本脚本不做语义判断。

五态：
  verified     可达 + 权威层(official/journal/preprint/media) + 字段完整
  partial      可达，但社区/博客层来源，或必填字段缺失
  unreachable  404/超时/反爬（needs_human_check，≠ 不存在）
  invalid      无 URL/DOI 或格式错误
  unverified   --offline 或跳过检查

纯标准库，跨平台（win32/linux/darwin），控频访问。
用法：
  python verify_refs.py --refs research_refs.json --out verify_report.md
  python verify_refs.py --claims '[{"title":"...","url":"https://...","source":"X","year":2026}]'
  python verify_refs.py --refs refs.json --offline        # 不联网，仅结构检查
  python verify_refs.py --refs refs.json --strict         # unreachable/invalid 视为失败(CI 用)
  python verify_refs.py --refs refs.json --profile medical # 医学信源预设(期刊层域名扩展+社区层降级警示)
  python verify_refs.py --refs refs.json --export bibtex,csv # 导出verified-only参考文献(bibtex)+全量台账(csv)

引用字段支持 url / doi / pmid / arxiv 四选一（pmid 自动解析为 PubMed 页面，arxiv 自动解析为
arXiv abs 页面），去重覆盖 URL+DOI+PMID 及 arXiv 解析后的 URL。
v1.5：arXiv ID 元数据校验（export.arxiv.org 官方 API，不存在的 ID 直接判 invalid，
不被可达性检查误判 unreachable——沿用 DOI 元数据先行的判定顺序）；unreachable 条目
自动查 Wayback Machine 存档（有存档附对照链接，人工复核有抓手）。
v1.6：主机断路器（同一主机连续 2 次传输层失败 → 本批次跳过该主机外呼并诚实备注，
断网环境不再整批卡死）；可操作报错（超时给 --timeout 20 建议、DNS/拒连分类措辞、
待人工复核区加建议动作）；DOI↔PMID 交叉一致性（双键引用互证，抓「真 ID 拼接」伪造）；
期刊名一致性核查（复用 DOI 登记元数据，不符降 partial——抓「真 DOI 真论文假期刊」）。
v1.7：作者名一致性核查（复用 CSL author，任一姓氏命中即一致，全部不命中降 partial）；
能力边界矩阵（报告尾部结构化呈现已抓/未抓伪造类型）；--format html 自包含单文件报告
（零外链、移动端可读，给导师/编辑的分享件）。
v1.8：撤稿检测（Crossref/Retraction Watch API——真实存在的论文也可能已撤稿，
撤稿引用封顶 partial 并转入人工复核）；OpenAlex 书目级存在性核查（无 DOI/PMID/arXiv
的引用多一路正面确认信号，只确认不降级——收录有滞后，查无 ≠ 编造）；元数据端点
UA 轮换重试（403/406 韧性）；--easy 医学误触发修复。
v1.9：Semantic Scholar 第三源交叉确认（DOI 元数据获取失败时的第二路正面信号——
只确认不降级，S2 记录质量参差实测有误记，绝不以其不一致作负面判据）；
BibTeX 导入（--refs refs.bib 自动识别，Zotero/EndNote 导出文件零改造直查）；
OpenAlex API key 支持（2026-02 起生产调用需 key：--openalex-key 或环境变量）；
--mailto 进入 Crossref polite pool（机构用户限速更宽松）+ 429 Retry-After 遵从；
投稿前结论（arXiv 2026-05 起对含幻觉/未核引用投稿实施处罚——报告头部直接给出
可否提交的结论行）；--export auditjson 透明工作底稿（每条引用的逐项检查明细，
机器可读，回应"检测系统需要透明多源"的行业呼吁）。
v1.11：判定确定性保卫——arXiv API 偶发 406/403（批内多请求撞其反机器人窗口）
时不再静默跳过内容核验，指数退避重试后 fallback 官方着陆页 arxiv.org/abs/<id>
做标题比对（复用 0.50/0.82 阈值；着陆页 404 判 invalid），同一引用两次运行判定
不再漂移，并补齐与 DOI 路径（S2 第二源）的对称性；语义层工作底稿结构化
（semantic 字段支持 {claim, support, quote, note} 对象，auditjson/报告透出
semantic_audit 区；not_in_source/contradicted 封顶 partial+人工复核——把
「disclosing uncertainty」落成机器可读）；投稿前结论修正为 arXiv 2026-05 起
处罚并补会议（ICML 2026 桌拒）话术。
v1.10：引用级并行验证（--workers，默认 4——条与条相互独立，整批耗时约 ÷workers，
直攻「跨国数据库验证慢」）；全局网络降级模式（批内 ≥3 个不同主机传输层失败 →
其余外呼快速诚实跳过并给可操作建议，把「等很久」变成「快速结论」）；
Semantic Scholar 标题检索确认（无 DOI/PMID/arXiv 引用的第三路正面信号，只确认
不降级；query 连字符空格化——S2 官方文档确认连字符查询无结果）；批内结果缓存
（同 DOI/URL 二次出现复用判定，不重复外呼）；降级态快速失败（传输失败不再重试）。
v1.12：持久磁盘缓存（--cache 默认开，sqlite3 标准库存 ~/.cache/cite-holmes/，TTL 默认
168h——复跑不再出国、判定口径一致；--strict 强制绕过保 CI 诚实；--refresh-cache
强制重验）；--proxy 显式代理；能力矩阵新增「不支持输入」行；包内私有工具清除。"""

# v6.0.0 模块化分层壳：按本文件所在目录加载各自的 ch_* 实例——
# trunk 与 mcp 副本互不共享模块对象（防双壳 _bind 互踩）；
# 一切跨层符号经 _ROOT（=本壳命名空间）解析，测试 patch vr.X 直接生效。
import os as _os, sys as _sys, importlib.util as _ilu

import sys


def main_with_args(argv: list) -> int:
    """程序化调用入口（测试/其他脚本用）。argv 不含脚本名。"""
    old = sys.argv
    sys.argv = [sys.argv[0]] + list(argv)
    try:
        return main()
    finally:
        sys.argv = old


_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PREFIX = "mcp_" if _os.path.basename(_HERE) == "mcp" else ""
_LAYERS = ["ch_text", "ch_netio", "ch_registry", "ch_semantic", "ch_verify", "ch_reports", "ch_cli"]
for _name in _LAYERS:
    _spec = _ilu.spec_from_file_location(_PREFIX + _name, _os.path.join(_HERE, _name + ".py"))
    _mod = _ilu.module_from_spec(_spec)
    _sys.modules[_spec.name] = _mod
    _spec.loader.exec_module(_mod)
    _mod._bind(_sys.modules[__name__])
    globals()[_name] = _mod
for _name in _LAYERS:
    for _k, _v in list(vars(globals()[_name]).items()):
        if not _k.startswith("__"):
            globals()[_k] = _v


def main():
    # v6.0.0 审计 P1：必须走 globals 里已 _bind 的层实例——真 import 语句会经
    # sys.path 解析到第二个未 bind 的 ch_cli（mcp 目录形态下 CLI 必炸）
    return ch_cli.main()


# __all__ 真末尾重算：import * 消费者拿到全部公开+单下划线名
_NAMES = [n for n in dir() if not n.startswith("__")]
__all__ = _NAMES
del _NAMES

if __name__ == "__main__":
    sys.exit(main())
