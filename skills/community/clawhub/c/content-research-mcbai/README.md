# content-research — Tìm kiếm bài viết & tin tức trending

> Skill OpenClaw tự động tìm kiếm bài viết, tin tức và nguồn nội dung về bất kỳ chủ đề nào từ web. Sử dụng **Brave Search + Tavily** song song để cho kết quả phong phú nhất. Thường dùng trước `content-writer` để chuẩn bị nguồn bài.

---

## Skill này dùng để làm gì?

Trước khi viết một bài LinkedIn hay, bạn cần nguồn bài chất lượng. Skill này giúp bạn:
- Tìm nhanh 10-15 bài viết mới nhất về bất kỳ chủ đề nào
- Lọc theo loại nguồn: news, blog, LinkedIn, YouTube
- Tự động gắn tag (AI, Funding, SaaS, Startup...) để dễ lựa chọn
- Kết hợp 2 search engine (Brave + Tavily) để không bỏ sót bài hay

---

## Tính năng

| Tính năng | Chi tiết |
|-----------|---------|
| 🔍 Dual Search Engine | Brave Search + Tavily chạy song song |
| 🔄 Fallback tự động | Nếu 1 engine lỗi → dùng engine còn lại |
| 🏷️ Auto-tag | Tự động gắn tag: AI, Funding, SaaS, Tools, Trends, Startup, Growth |
| 📰 Phân loại nguồn | News / Blog / Report / Video / LinkedIn |
| 🗑️ Dedup tự động | Loại bỏ bài trùng lặp giữa 2 engine |
| 🔗 Tích hợp | Kết nối trực tiếp với `content-writer` |

---

## Cài đặt

### Yêu cầu
- OpenClaw đã cài đặt
- Brave Search API key (miễn phí 1,000 req/tháng)
- Tavily API key (miễn phí 1,000 req/tháng)

### Cấu hình API keys

**Brave Search** — đã tích hợp sẵn trong OpenClaw. Cấu hình qua:
```powershell
openclaw configure --section web
```

**Tavily** — thêm vào file `.env` của OpenClaw:
```
# File: ~/.openclaw/.env
TAVILY_API_KEY=tvly-your-key-here
```

Lấy Tavily API key miễn phí tại: [tavily.com](https://tavily.com)

### Copy skill vào OpenClaw

```powershell
# Windows
Copy-Item -Recurse content-research $env:USERPROFILE\.agents\skills\

# macOS / Linux
cp -r content-research ~/.agents/skills/
```

---

## Cách dùng

### Cơ bản
```
Research chủ đề: AI agents 2026
```

### Tùy chỉnh nguồn
```
Tìm bài về "OpenAI funding" chỉ từ news, 1 tuần gần đây

Research "AI marketing tools" từ blog, lấy 15 bài
```

### Kết quả mẫu

```
## Research Results: "AI agents 2026"
Found 14 articles from 11 sources
Sources: Brave (8) + Tavily (9) → merged 14 unique

### 📰 News
1. OpenAI Launches New Agent Framework — TechCrunch (2 hours ago) [Tavily]
   OpenAI announced a major update to its agent infrastructure...
   🏷️ AI | 🔗 techcrunch.com/...

### 📝 Articles & Blogs
2. The State of AI Agents in 2026 — a16z (3 days ago) [Brave]
   ...
```

---

## Tích hợp với content-writer

Sau khi có kết quả, chọn bài muốn dùng và chuyển sang viết:
```
Dùng bài 1, 3, 5 để viết LinkedIn post
```

Agent sẽ tự động gọi `content-writer` với các bài đã chọn.

---

## Cấu trúc files

```
content-research/
├── README.md              ← Bạn đang đọc
├── SKILL.md               ← Điều khiển agent
└── references/
    └── source-filters.md  ← Cấu hình filter nguồn chi tiết
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
