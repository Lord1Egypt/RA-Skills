#!/usr/bin/env python3
"""search_eu_ctr.py - EU Clinical Trials Register (legacy EudraCT) search / EU-CTR 检索.

2026-09-07 上移改造：抓取逻辑已从本文件（随技能包发布的本地代码）上移到 Coze
服务端节点（euctr_search_node，纯 HTTP HTML 解析），本文件改为**薄壳**——
转发 ``search_ictrp.py --source euctr``（统一端点，共享 ICTRP token），与
chiCTR/ISRCTN/DRKS/CTIS 同构。

上移动机：EudraCT 为服务端渲染 HTML，解析器属实现资产（站点改版只需改服务端
一处、用户免更新），且页面结构知识不应随技能包发布泄露。

⚠️ 依赖部署：统一端点须已部署 euctr 节点（sources.py 白名单 + search_node 分支）
才返回真实数据；未部署时返回空并提示。无本地降级路径（抓取执行器已上 Coze，
本地不再保留 HTML 解析资产，符合 §20.14 "词表留本地、上移抓取执行器"）。

覆盖范围：EudraCT 存量 2004-2022+ 欧盟试验。2022 起新试验在 CTIS
（euclinicaltrials.eu，公开 REST JSON 无认证——见 search_ctis.py；2026-09-07 实测
CTIS 公开 API 无需 OAuth2，OAuth2 仅 sponsor/监管 workspace 用）。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import search_ictrp  # noqa: E402


if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--source", "euctr"] + sys.argv[1:]
    search_ictrp.main()
