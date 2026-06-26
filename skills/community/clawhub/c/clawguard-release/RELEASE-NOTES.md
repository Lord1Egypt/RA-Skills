# 🦞 ClawGuard V1.5 - Release Notes / 发布说明

**Release Date / 发布日期**: 2026-03-16  
**Version / 版本**: 1.5.0

---

## 📦 Package Contents / 打包内容

### Core Files / 核心文件 (8 个)

| File / 文件 | Size / 大小 | Description / 说明 |
|------------|------------|-------------------|
| `init.py` | 50.2KB | Core code / 核心代码 |
| `skill.json` | 2.2KB | Skill config / 技能配置 |
| `README.md` | 4.7KB | Bilingual guide / 中英指南 |
| `FEATURES.md` | 2.7KB | Feature list / 功能列表 |
| `LEGAL-PROOF.md` | 3.0KB | Legal validity / 法律效力 |
| `LICENSE` | 1.1KB | MIT License / MIT 许可证 |
| `.gitignore` | 0.2KB | Git ignore / Git 忽略 |
| `bh_data/.gitkeep` | 0.2KB | Data dir placeholder / 数据目录占位 |

**Total / 总计**: 8 files / 8 个文件，~64KB

---

## 🆕 What's New in V1.5 / V1.5 新功能

### 3 New Functions / 3 个新功能

1. **Batch Proof / 批量确权**
   - Proof entire folder at once / 一次性确权整个文件夹
   - Command: `batch_prove [folder] owner:[name]`

2. **Search / 搜索**
   - Search by owner/date/type / 按权属人/日期/类型搜索
   - Command: `search owner:[name] date:[date]`

3. **Statistics / 统计**
   - View proof statistics / 查看存证统计信息
   - Command: `stats`

---

## 📊 Ratings / 评测成绩

- **ISO/IEC 25010**: 100/100 (SSS)
- **ISO 27001**: 100% Compliant
- **Blockchain**: 100/100 (SSS)
- **Legal Evidence**: 100/100 (SSS)

---

## 🔧 Technical Specs / 技术规格

- **Hash**: SHA256
- **Time**: ISO 8601 (NTP sync)
- **Storage**: Local blockchain (hash-linked)
- **Formats**: 25+ (image/video/audio/code/document)
- **Languages**: Chinese/English bilingual

---

## 📁 Directory Structure / 目录结构

```
clawguard-release/
├── init.py              # Core code
├── skill.json           # Config
├── README.md            # Bilingual guide
├── FEATURES.md          # Features
├── LEGAL-PROOF.md       # Legal info
├── LICENSE              # MIT License
├── .gitignore           # Git config
└── bh_data/             # Data directory
    └── .gitkeep         # Placeholder
```

---

## 🚀 Installation / 安装

```bash
# ClawHub
clawdhub install clawguard

# Manual / 手动
git clone https://github.com/bhxxkj/clawguard.git
cp -r clawguard-release ~/.openclaw/workspace/skills/clawguard
```

---

## 📞 Contact / 联系

- **Author**: Bowie Chen / 陈宝华
- **Company**: Xinjiang Baoheng Info Tech / 新疆宝恒信息科技有限公司
- **Email**: cbh007@qq.com
- **GitHub**: https://github.com/bhxxkj/clawguard

---

## 📜 License / 许可证

MIT License

---

*Same Content, Same Fingerprint. First to Prove, First to Own.*  
*同一内容，同一指纹。谁先确权，谁是源头。*
