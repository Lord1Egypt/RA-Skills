#!/usr/bin/env python3
"""search_ctis.py - EU CTIS (Clinical Trials Information System) search / CTIS 检索.

CTIS = EudraCT 的继任者（Regulation (EU) 536/2014，2022-01 起的新欧盟临床试验）。
2026-09-07 实测：CTIS 提供**公开无认证的 REST JSON API**
（https://euclinicaltrials.eu/ctis-public-api，POST /search + GET /retrieve/{ctNumber}），
不需要 OAuth2（OAuth2 仅 sponsor/监管 workspace 用）。检索逻辑已上移 Coze 服务端
（ctis_search_node + ctis_scrape_details_node），本文件为**薄壳**——转发
``search_ictrp.py --source ctis``（统一端点，共享 ICTRP token），与
chiCTR/ISRCTN/DRKS/EUCTR 同构。

上移动机：CTIS 的 JSON API 契约/状态码表/字段映射属实现资产，不随技能包发布；
站点改版只改服务端一处、用户免更新。

⚠️ 依赖部署：统一端点须已部署 ctis 节点（sources.py 白名单 + search_node /
scrape_details_node 分支）才返回真实数据。无本地直连降级（CTIS 无本地旧抓取器——
公开 API 本就该走服务端统一出口，避免每家技能重复实现）。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import search_ictrp  # noqa: E402


if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--source", "ctis"] + sys.argv[1:]
    search_ictrp.main()
