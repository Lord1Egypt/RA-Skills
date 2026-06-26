# 万能祝福语生成器

> 输入节日/对象/风格，AI 生成个性化祝福语。覆盖全年所有节日和人生重要场合。

## ✨ 支持场景
春节、妇女节、儿童节、光棍节、圣诞节、生日、婚礼、乔迁、升学、毕业... 全部搞定

## 🚀 快速开始
```bash
export DEEPSEEK_API_KEY=your_key

# 生成妇女节祝福
python3 scripts/generate_blessing.py --festival "妇女节" --target "妈妈" --style "温情"

# 生成光棍节幽默祝福
python3 scripts/generate_blessing.py --festival "光棍节" --target "闺蜜" --relation "平辈" --recent "刚失恋" --style "幽默"

# 生成春节正式祝福
python3 scripts/generate_blessing.py --festival "春节" --target "老板" --relation "上级" --style "正式" --length "short"
```

## 参数说明
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--festival` | 节日/场合（必填） | — |
| `--target` | 祝福对象 | 朋友 |
| `--relation` | 关系：长辈/平辈/晚辈/上级/客户 | 平辈 |
| `--recent` | 近况关键词 | — |
| `--style` | 风格：正式/温情/幽默/文艺/押韵 | 温情 |
| `--length` | 字数：short/medium/long | medium |

## 📝 作者
[antonia-sz](https://github.com/antonia-sz) · MIT License
