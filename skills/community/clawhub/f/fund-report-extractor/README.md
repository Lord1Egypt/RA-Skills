# 基金报告提取工具使用说明

## 快速开始

```bash
python skills/fund-report-extractor/extract.py --code 006567 --name "中泰星元"
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| --code | 基金代码 | 006567, 260101 |
| --name | 基金名称 | 中泰星元、景顺长城优选 |

## 输出

- `reports_{代码}/` - 原始报告文件
- `{名称}_投资策略汇总.txt` - 完整汇总

## 示例

```bash
# 提取中泰星元
python skills/fund-report-extractor/extract.py --code 006567 --name "中泰星元"

# 提取景顺长城优选混合
python skills/fund-report-extractor/extract.py --code 260101 --name "景顺长城优选混合"
```

## 依赖

```bash
pip install akshare pymupdf pdfplumber pandas requests
```

## 注意事项

1. 网络请求可能失败，可重试
2. 部分PDF是扫描版，可能提取不完整
3. 东方财富只保留最近4年报告
