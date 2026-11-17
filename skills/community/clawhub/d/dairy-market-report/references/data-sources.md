# 数据源与获取方式

报告各章节所引用的官方/行业数据源. 优先级: 1) 艾格农业月报 (主输入), 2) 农业农村部, 3) 海关总署, 4) 国际机构.

---

## 国内 (China)

| 数据 | 来源 | 频次 | URL/获取方式 |
|---|---|---|---|
| 生鲜乳价格 (10 主产省) | 农业农村部畜牧兽医局 | 月度 | https://www.moa.gov.cn 通知公告 |
| 玉米 / 豆粕 / 青贮 价格 | 农业农村部; 艾格农业监测 | 月度 | 同上 |
| 生鲜乳产量 | 国家统计局 | 月度 (季度发布) | https://www.stats.gov.cn |
| 乳制品产量 (分品类) | 国家统计局 | 月度 | 同上 |
| 乳制品进口 / 出口 (分品类) | 海关总署 | 月度 | http://www.customs.gov.cn |
| 婴配粉进口 / 出口 | 海关总署 | 月度 | 同上 |
| 汇率 (CNY/USD 中间价) | 中国人民银行 | 日度 | http://www.pbc.gov.cn |
| 乳品政策 | 农业农村部 / 市场监管总局 / 卫健委 | 不定期 | 各部委官网 |
| 乳企动态 | 上市公司公告 (巨潮) | 实时 | http://www.cninfo.com.cn |

---

## 国际 (Overseas)

| 数据 | 来源 | 频次 | URL |
|---|---|---|---|
| GDT 拍卖结果 (价格/成交) | Fonterra GDT | 半月 (周二) | https://www.globaldairytrade.events |
| 新西兰生鲜乳产量 | DCANZ (Dairy Companies Association of New Zealand) | 月度 | https://www.dcanz.com |
| 新西兰农场收购价 | Fonterra Farmgate Milk Price | 季度 | https://www.fonterra.com |
| 澳大利亚生鲜乳产量 | Dairy Australia | 月度 | https://www.dairyaustralia.com.au |
| 澳大利亚农场收购价 | Dairy Australia | 半年 | 同上 |
| 美国 生鲜乳价格 (All-Milk) | USDA NASS | 月度 | https://www.nass.usda.gov |
| 美国 生鲜乳产量 | USDA NASS | 月度 | 同上 |
| 欧盟 牛奶价格 | AHDB / Eurostat | 半月 / 月度 | https://ahdb.org.uk / https://ec.europa.eu/eurostat |
| 欧盟 生鲜乳产量 | Eurostat / EuroMilk | 月度 | 同上 |
| 全球乳制品供需平衡 | USDA FAS PSD Online | 年度 + 半年更新 | https://apps.fas.usda.gov/psdonline |
| 期货 (WMP/SMP/Butter) | NZX (新西兰) / EEX (欧洲) / CME (美国) | 日度 | https://www.nzx.com |

---

## 第三方监测与商业数据源 (可选)

| 数据 | 来源 | 备注 |
|---|---|---|
| 国内现货价 (大包粉/黄油) | 艾格农业现货监测 | 月报核心数据 |
| 国内 乳企库存 | 艾格农业访谈 + 上市公司财报推算 | 月度推断 |
| 港口到岸价 (CIF) | 海关 + 卓创资讯 / 钢联 | 可补充 |
| 终端零售价 | 凯度 / 尼爾森 / 艾瑞 | 季度 |

---

## 数据使用原则

1. **官方优先** - 海关 / 农业农村部 / 国家统计局 优先于商业源.
2. **同期对比** - 同比 + 环比 都要有; 同比基期为去年同月.
3. **汇率统一** - 所有跨币种对比, 用央行月度中间价均值.
4. **YTD 累计** - 进口/出口 用 年初至今 累计, 避免单月波动.
5. **不一致时** - 若两个源数字差异 >2%, 在 AI 解读中说明, 优先采信官方.
