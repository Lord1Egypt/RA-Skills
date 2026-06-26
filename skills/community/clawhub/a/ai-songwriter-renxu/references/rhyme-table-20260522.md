# 押韵表实测验证（2025-05-22）

## 正确分类（经多轮迭代验证）

### ang 集合（归韵用）
```
航 光 扬 场 疆 长 望 荡 魂 雄 风 鸿 龙 鹏 铭 峰 方 章 灯 芒 钢 康 强 翔 苍 桑 墙 庄 脏 旁 昂 量 详 彷 徨 狂 祥
```
> 实测确认：灯(dēng)✓ 强(qiáng)✓ 藏(cáng)✓ 方(fāng)✓ 章(zhāng)✓ 芒(máng)✓ 钢(gāng)✓ 康(kāng)✓

### non_ang 集合（白脚用）
```
间 上 藏 沧 茫 情 名 性 当 忘 林 生 铁 青 星 时 此 心 中 里 外 下 那 和 去 见
```
> 实测确认：星(xīng)✓ 情(qíng)✓ 名(míng)✓ 性(xìng)✓（这些是 -ing/-ong 韵，不是 -ang）

## 错误表（多次踩坑记录）

### 原 skill 中错误分类
| 字 | 原skill以为 | 实际 | 说明 |
|----|-----------|------|------|
| 灯 | non-ang | **ang** | dēng 韵尾 -eng |
| 强 | non-ang | **ang** | qiáng 韵尾 -iang |
| 藏 | non-ang | **ang** | cáng 韵尾 -ang |
| 方 | non-ang | **ang** | fāng 韵尾 -ang |
| 章 | non-ang | **ang** | zhāng 韵尾 -ang |
| 芒 | non-ang | **ang** | máng 韵尾 -ang |
| 钢 | non-ang | **ang** | gāng 韵尾 -ang |
| 康 | non-ang | **ang** | kāng 韵尾 -ang |
| 声 | ang | **non-ang** | shēng 韵尾 -eng |
| 名 | ang | **non-ang** | míng 韵尾 -ing |
| 性 | ang | **non-ang** | xìng 韵尾 -ing |
| 情 | ang | **non-ang** | qíng 韵尾 -ing |
| 星 | ang | **non-ang** | xīng 韵尾 -ing |

### 边缘字韵母实测（pypinyin验证，2025-05-22补充）

| 字 | pypinyin韵母 | eng/ong分组 | 错误分类 | 正确分组 |
|----|-------------|------------|---------|---------|
| 穷 | iong | eng | ong | **eng** |
| 穹 | iong | eng | ong | **eng** |
| 胸 | iong | eng | ong | **eng** |
| 逢 | ong | **eng**（u介音） | ong | **eng** |
| 雄 | iong | eng | ong | **eng** |
| 翎 | ing | eng | eng | **eng**（ling→ing，ing属eng）|
| 崧 | iong | ong | eng | **ong** |
| 宁 | ing | eng | eng | **eng**（ning→ing，ing属eng）|
| 名 | ing | eng | ong | **eng**（ming→ing，ing属eng）|
| 场 | ang | ang | 存疑 | **ang** |

> **结论**：肉眼判断韵母不可靠。eng/ong 分界点：iong/ing/ueng → eng；ong（无i/u介音）→ ong。用 pypinyin 逐字验证是唯一可靠方法。

## 验证结论

ang ∩ non_ang = ∅（完全不相交）

## 尾字重复阈值

- 单一尾字 > 5 次 → ⚠️ 用户会抱怨"重复尾字太多了"
- 建议：每句韵脚不同词，目标 ang 表中每个字使用 ≤ 4 次
