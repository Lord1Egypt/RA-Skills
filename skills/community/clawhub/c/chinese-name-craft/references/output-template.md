# 输出模板与 JSON Schema

## Word 文档生成

起名分析完成后，将结果组装为 JSON 文件，然后调用脚本生成 Word 文档：

```bash
python scripts/generate_doc.py <input.json> [output.docx]
```

## JSON Schema

```json
{
  "title": "《X先生Y女士之子》定名方案",
  "greeting": "祝贺语...",
  "father_name": "父亲姓名",
  "mother_name": "母亲姓名",
  "child_label": "之子/之女",

  "basic_info": [
    "姓　名：...",
    "性　别：...",
    "公　历：...",
    "农　历：...",
    "生　肖：...",
    "纳　音：..."
  ],

  "bazi": {
    "shishen": ["十神", "年", "月", "日柱", "时"],
    "tiangan": ["天干", "年", "月", "日", "时"],
    "dizhi":   ["地支", "年", "月", "日", "时"],
    "wuxing":  ["五行", "年五行", "月五行", "日五行", "时五行"],
    "canggan": ["藏干", "年藏", "月藏", "日藏", "时藏"]
  },

  "wuxing_stats": [
    "金：X = N",
    "木：X = N",
    "火：X = N",
    "水：X",
    "土：X"
  ],

  "need_wuxing": "土、金",

  "expert_comment": [
    "性格分析...",
    "事业分析...",
    "财运分析...",
    "婚姻分析...",
    "健康提示...",
    "宜忌属相...",
    "事业方向...",
    "有利要素..."
  ],

  "names": [
    {
      "title": "定名一：《姓名》",
      "wuge": {
        "tian": "天格数", "ren": "人格数", "di": "地格数",
        "wai": "外格数", "zong": "总格数",
        "tian5": "天格五行", "ren5": "人格五行", "di5": "地格五行",
        "wai5": "外格五行", "zong5": "总格五行"
      },
      "sancai": "（X、Y、Z）三才配置吉凶评价",
      "ziyi": ["字义1...", "字义2..."],
      "jingyi": ["经意1...", "经意2..."],
      "yinlv": "姓XIAO(声调) 名1YI(声调) 名2CHEN(声调)",
      "yinlv_comment": "音律评价...",
      "shuli": [
        "人格N：含义。（吉凶）",
        "基业：...",
        "家庭：...",
        "健康：...",
        "含义：...",
        "地格N：...",
        "总格N：...",
        "外格N：..."
      ],
      "chuangyi": "生肖喜忌关联 + 整体寓意解读..."
    }
  ],

  "summary_title": "《名一》《名二》《名三》",
  "summary": ["综合评价..."],
  "disclaimer": "注：以上释解出自《易经》中《姓名学》理论对人一生的暗示导理。仅作探讨与参考！"
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| title | 否 | 文档标题，默认"定名方案" |
| greeting | 否 | 开头祝贺语 |
| father_name | 是 | 父亲姓名（用于自动文件名） |
| mother_name | 是 | 母亲姓名（用于自动文件名） |
| child_label | 否 | "之子"或"之女"，默认"之子" |
| basic_info | 是 | 基本信息行列表 |
| bazi | 是 | 八字四柱数据（5行x4列） |
| wuxing_stats | 是 | 五行统计行列表 |
| need_wuxing | 是 | 需补五行 |
| expert_comment | 是 | 专家点评段落列表 |
| names | 是 | 候选名字数组（建议3组） |
| names[].wuge | 是 | 五格数理（5格数字+5格五行） |
| names[].sancai | 是 | 三才配置评价 |
| names[].ziyi | 是 | 字义原理列表 |
| names[].jingyi | 是 | 经意原理列表 |
| names[].yinlv | 是 | 音律标注 |
| names[].yinlv_comment | 否 | 音律评价 |
| names[].shuli | 是 | 数理分析列表 |
| names[].chuangyi | 是 | 创意定位 |
| summary_title | 否 | 总评标题 |
| summary | 是 | 总评段落列表 |
| disclai