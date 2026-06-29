# Official Document Format Standards

> Based on GB/T 9704-2012 (Formats for Party and Government Official Documents) and enterprise-general standards.

## 1. Page Setup

| Item | Standard | Notes |
|------|----------|-------|
| Paper | A4 (210mm × 297mm) | General standard |
| Top margin | 37mm ± 1mm | Header space |
| Bottom margin | 35mm ± 1mm | Footer space |
| Left margin | 28mm ± 1mm | Binding edge |
| Right margin | 26mm ± 1mm | Flipping edge |

## 2. Font & Size Standards

| Element | Font | Size | Alignment | Notes |
|---------|------|------|-----------|-------|
| **Title** | FangZheng XiaoBiaoSong / HeiTi | No.2 (22pt) | Centered | Subtitle: No.2-in-small KaiTi |
| **L1 Heading** | HeiTi | No.3 (16pt) | Left-aligned | 一、二、三、… |
| **L2 Heading** | KaiTi_GB2312 | No.3 (16pt) | 2-char indent | （一）（二）（三）… |
| **L3 Heading** | FangSong_GB2312 | No.3 (16pt) | 2-char indent | 1. 2. 3. … |
| **L4 Heading** | FangSong_GB2312 | No.3 (16pt) | 2-char indent | (1) (2) (3) … |
| **Body** | FangSong_GB2312 | No.3 (16pt) | 2-char indent | — |
| **Signature unit** | FangSong_GB2312 | No.3 (16pt) | Right-aligned | 2 blank lines above |
| **Signature date** | FangSong_GB2312 | No.3 (16pt) | Right-aligned | Arabic numerals |
| **Attachment title** | FangSong_GB2312 | No.3 (16pt) | Blank line below body | "附件：1. ×××" |
| **Attachment content** | FangSong_GB2312 | No.3 (16pt) | — | Independent layout |
| **CC list** | FangSong_GB2312 | No.4 (14pt) | Bottom of signature page | 抄送：××× |
| **Page number** | FangSong | No.4 (14pt) | Bottom center | "- 1 -" format |

## 3. Paragraph & Line Spacing

| Item | Standard |
|------|----------|
| **Line spacing** | Fixed 28pt (including 3pt before/after) |
| **Paragraph indent** | First line 2 characters (~32pt) |
| **Paragraph spacing** | 0pt before, 0pt after (0.5 line between heading levels if needed) |
| **Heading spacing** | One blank line above title, one blank line below before body |

## 4. Heading Hierarchy

```
┌─────────────────────────────────────────────────────┐
│            Document Title (No.2 HeiTi centered)        │
│        —— Subtitle (small No.2 KaiTi, optional)       │
│                                                     │
│ Recipient (No.3 FangSong, left-aligned):           │
│                                                     │
│  一、L1 Heading (No.3 HeiTi, left-aligned)           │
│    （一）L2 Heading (No.3 KaiTi, 2-char indent)      │
│      1. L3 Heading (No.3 FangSong, 2-char indent)   │
│        (1) L4 Heading (No.3 FangSong, 2-char indent)│
│                                                     │
│  Body paragraph (No.3 FangSong, 2-char indent,      │
│  line spacing 28pt)                                  │
│                                                     │
│  二、L1 Heading                                       │
│    ……                                               │
│                                                     │
│                                      Department        │
│                                      June 11, 2026    │
└─────────────────────────────────────────────────────┘
```

## 5. Heading Numbering Rules

| Level | Format | Example |
|-------|--------|---------|
| L1 | 一、二、三、… | 一、高度重视，加强组织领导 |
| L2 | （一）（二）（三）… | （一）明确责任分工 |
| L3 | 1. 2. 3. … | 1. 建立健全工作机制 |
| L4 | (1) (2) (3) … | (1) 细化落实措施 |
| L5 | ① ② ③ … | ① 定期检查督促 |

## 6. Signature & Date

| Element | Standard |
|---------|----------|
| **Signing unit** | 2 blank lines above body end, right-indented 2 chars, full official name |
| **Date of issue** | Right-indented 2 chars, Arabic numerals (2026年6月11日) |
| **Seal position** | Red seal overlapping date (can be omitted in electronic copies) |

## 7. Attachment Format

```
One blank line below body, left-indented 2 chars:
附件：1. ××××××××××××××
       2. ××××××××××××××
       (Multiple attachments aligned by number)
```

## 8. Page Numbering

| Item | Standard |
|------|----------|
| Position | Below the page body, centered in footer |
| Size | No.4 half-width Song font |
| Format | - 1 -, - 2 -, - 3 - … |
| Start | From the first page of body text |
| Blank pages | No page number on blank pages and pages after blank pages |
| Odd pages | Right-aligned, one space from right |
| Even pages | Left-aligned, one space from left |

## 9. Common Formal Vocabulary

| Term | Usage | Example |
|------|-------|---------|
| 兹 | Opening, meaning "now" | 兹收到贵单位来函…… |
| 鉴于 | Introducing background/reason | 鉴于当前项目进度…… |
| 经研究 | Indicates decision after study | 经研究，现批复如下： |
| 为…… | Introducing purpose | 为进一步加强…… |
| 现就……通知如下 | Transitional phrase | 现就有关事项通知如下： |
| 请遵照执行 | Notice/regulation closing | 以上规定，请遵照执行。 |
| 妥否，请批示 | Request closing | 妥否，请批示。 |
| 特此函达 | Letter closing | 特此函达。 |
| 此复 | Reply closing | 此复。 |
| 特此通知 | Notice closing | 特此通知。 |

## 10. Closing Phrases by Document Type

| Type | Common Closing |
|------|---------------|
| Notice | 特此通知。/ 请遵照执行。/ 请各单位认真落实。 |
| Request | 妥否，请批示。/ 以上请示，请予审批。 |
| Report | 特此报告。/ 以上报告，请审阅。/ 如有不妥，请指正。 |
| Letter (consultation) | 特此函商。/ 如无不妥，请予支持。 |
| Letter (reply) | 特此函复。/ 此复。 |
| Letter (invitation) | 敬请届时参加。/ 特此函请。 |
| Approval | 此复。/ 特此批复。/ 请遵照执行。 |
| Meeting Minutes | 以上纪要精神，请各单位认真贯彻落实。 |
| Work Summary | 特此总结。/ 以上为×××工作总结，请批评指正。 |
| Plan | 请各单位结合实际认真贯彻落实。 |
| Proposal | 希望大家积极响应，共同……/ 让我们…… |
| Commendation | 特此通报表彰。/ 希望受表彰的单位和个人再接再厉。 |
| Debriefing | 以上述职，请予评议。/ 不妥之处，请批评指正。 |
| Explanation | 特此说明。/ 以上情况，如实反映。 |
| Application | 特此申报，请予审批。/ 以上申报，请审阅。 |