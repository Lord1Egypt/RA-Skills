# content-writer — Viết post cho mọi nền tảng mạng xã hội

> Skill OpenClaw tạo post chất lượng cao cho **LinkedIn, Facebook, Twitter/X, TikTok, Threads** từ bất kỳ nguồn bài nào. Hỗ trợ **6 format, 8 tone, 2 ngôn ngữ**. Output plain text sẵn sàng đăng — không cần chỉnh sửa thêm.

---

## Skill này dùng để làm gì?

Bạn có ý tưởng, bài nghiên cứu, hoặc data hay — nhưng viết post tốn quá nhiều thời gian? Skill này giúp bạn:
- Biến bất kỳ nguồn bài nào thành post đăng ngay
- Chọn đúng format cho từng nền tảng (Facebook cần Story/Hook-List, LinkedIn cần Toplist/POV)
- Điều chỉnh tone phù hợp mục tiêu (viral, giáo dục, kể chuyện, phân tích...)
- Viết tiếng Anh hoặc tiếng Việt tự nhiên
- Output chuẩn ngay — không markdown, không format lạ

---

## Nền tảng hỗ trợ

| Nền tảng | Style | Format phù hợp |
|----------|-------|----------------|
| LinkedIn | Professional, data-driven | Toplist, POV, Case Study, How-to |
| Facebook | Conversational, emotional | Story, Hook-List-CTA, POV |
| Twitter/X | Punchy, opinionated | POV ngắn, Hook-List ngắn |
| TikTok | Casual, FOMO | Hook-List-CTA, How-to ngắn |
| Threads | Casual, unfiltered | POV, Story ngắn |

---

## 6 Format có sẵn

### 📋 Toplist
Danh sách có số thứ tự với data points.
```
HOOK: Bold claim + số cụ thể
CONTEXT: Tại sao quan trọng
LIST: Numbered items + metric
TAKEAWAY: Pattern rút ra
CTA: Câu hỏi engagement
```

### 💡 POV
Quan điểm táo bạo, có data hỗ trợ. Tạo tranh luận.
```
HOOK: Contrarian opening
DATA: Bằng chứng số liệu
ANALYSIS: Ý nghĩa
PREDICTION: Dự đoán rõ ràng
CTA: Câu hỏi kích comment
```

### 🏢 Case Study
Deep-dive một câu chuyện cụ thể.
```
HOOK: Metric ấn tượng nhất
CONTEXT: Vấn đề ban đầu
WHAT THEY DID: Chiến lược + số
RESULTS: Kết quả cụ thể
LESSON: Bài học không ai nói
CTA: Engagement question
```

### 🛠️ How-to
Hướng dẫn từng bước có thể làm ngay.
```
HOOK: Hứa hẹn kết quả rõ ràng
WHY: Người ta hay làm sai gì
STEPS: 3-7 bước action verbs
PRO TIP: Shortcut ít ai biết
RESULT: Đạt được gì
CTA: "Thử bước 1 ngay hôm nay"
```

### 📖 Story *(Facebook-optimized)*
Narrative cảm xúc, share rate cao.
```
OPENING SCENE: Khoảnh khắc cụ thể
TENSION: Xung đột leo thang
TURNING POINT: Aha moment
RESOLUTION: Kết quả + số liệu
LESSON: Non-obvious takeaway
CTA: Câu hỏi relatable / tag prompt
```

### 🎯 Hook-List-CTA *(Facebook viral)*
Format đơn giản, viral nhất Facebook.
```
HOOK (1 line): Stop-the-scroll
LIST: 5-10 items ngắn, cụ thể
CTA: Tag / Share / Comment prompt
```

---

## 8 Tone có sẵn

| Tone | Phong cách | Tốt cho |
|------|-----------|---------|
| Default | Data-driven, tự tin | Mọi nền tảng |
| Bold | Táo bạo, contrarian | LinkedIn, Twitter/X |
| Educational | Dạy học, dùng ví dụ | LinkedIn, Facebook |
| Storytelling | Kể chuyện, cảm xúc | Facebook, LinkedIn |
| Analytical | Phân tích, so sánh | LinkedIn, Twitter/X |
| Viral | FOMO, urgency, share-bait | Facebook, TikTok |
| Empathetic | Ấm áp, relatable, community | Facebook, Threads |
| Custom | Bạn tự mô tả | Mọi nền tảng |

---

## Cài đặt

```powershell
# Windows
Copy-Item -Recurse content-writer $env:USERPROFILE\.agents\skills\

# macOS / Linux
cp -r content-writer ~/.agents/skills/
```

---

## Cách dùng

### Đơn giản nhất
```
Viết post Facebook từ bài này: [paste nội dung]
```

### Chỉ định đầy đủ
```
Viết Story post Facebook, tone Viral, tiếng Việt, medium length từ bài này: [URL hoặc nội dung]
```

### Nhiều nền tảng cùng lúc
```
Viết cùng 1 nội dung thành 3 version: LinkedIn (Toplist), Facebook (Story), Twitter (POV ngắn)
```

### Sau khi research xong
```
Dùng bài 1 và 3 để viết Hook-List-CTA cho Facebook, tiếng Việt
```

---

## Quy tắc output

Post luôn là plain text thuần:
- Không asterisk (`*`) — không bao giờ
- Không markdown (`**`, `#`, `[]`)
- Không em dash (`—`) — dùng `-` hoặc dấu phẩy
- Không URL trong bài
- Nhấn mạnh bằng CAPS: `"Đây là CƠ HỘI thực sự"`
- List: dùng số hoặc `→` arrows
- Emoji: tự nhiên theo nền tảng (Facebook thoải mái hơn LinkedIn)

---

## Cấu trúc files

```
content-writer/
├── README.md                      ← Bạn đang đọc
├── SKILL.md                       ← Điều khiển agent
└── references/
    ├── brand-context.md           ← Brand identity MCB AI
    ├── platform-rules.md          ← Rules cho từng nền tảng
    ├── format-toplist.md          ← Format Toplist
    ├── format-pov.md              ← Format POV
    ├── format-case-study.md       ← Format Case Study
    ├── format-how-to.md           ← Format How-to
    ├── format-story.md            ← Format Story (Facebook)
    ├── format-hook-list-cta.md    ← Format Hook-List-CTA viral
    ├── tone-presets.md            ← 8 tone preset chi tiết
    └── formatting-rules.md        ← Rules bắt buộc
```

---

<p align="center">
  <a href="https://www.mcbai.vn">MCB AI</a> &nbsp;·&nbsp;
  <a href="https://www.youtube.com/@mcbaivn">YouTube</a> &nbsp;·&nbsp;
  <a href="https://openclaw.mcbai.vn">OpenClaw Cheatsheet</a> &nbsp;·&nbsp;
  <a href="https://openclaw.mcbai.vn/openclaw101">Khoá học OpenClaw 101</a> &nbsp;·&nbsp;
  <a href="https://www.facebook.com/groups/openclawxvn">Cộng đồng Facebook</a> &nbsp;·&nbsp;
  <a href="https://zalo.me/g/mmqkhi259">MCB AI Academy (Zalo)</a>
</p>
