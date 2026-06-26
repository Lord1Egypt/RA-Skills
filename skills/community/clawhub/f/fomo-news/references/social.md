# Social Posts

Tracks influential tech/AI figures via Google News RSS feeds and official company blogs.

## Command

```bash
node fetch.mjs social [--limit <n>] [--json]
```

## Tracked Figures

### Influential People
| Name | Handle | Category |
|------|--------|----------|
| Sam Altman | @sama | AI |
| Elon Musk | @elonmusk | Tech |
| Donald Trump | @realDonaldTrump | Politics |
| Jensen Huang | @nvidia | Tech |
| Dario Amodei | @DarioAmodei | AI |
| Satya Nadella | @satyanadella | Tech |
| Sundar Pichai | @sundarpichai | Tech |
| Mark Zuckerberg | @finkd | Tech |

### AI Lab Leaders
| Name | Handle | Category |
|------|--------|----------|
| Demis Hassabis | @demishassabis | AI |
| Yann LeCun | @ylecun | AI |
| Ilya Sutskever | @ilyasut | AI |
| Andrej Karpathy | @karpathy | AI |
| Arthur Mensch | @arthurmensch | AI |

### Tech CEOs
| Name | Handle | Category |
|------|--------|----------|
| Tim Cook | @tim_cook | Tech |
| Andy Jassy | @ajassy | Tech |
| Lisa Su | @LisaSu | Tech |

### AI Researchers & Thought Leaders
| Name | Handle | Category |
|------|--------|----------|
| Geoffrey Hinton | @geoffreyhinton | AI |
| Fei-Fei Li | @drfeifei | AI |
| Andrew Ng | @AndrewYNg | AI |
| Emad Mostaque | @EMostaque | AI |

### AI Investors
| Name | Handle | Category |
|------|--------|----------|
| Marc Andreessen | @pmarca | Tech |
| Vinod Khosla | @vkhosla | Tech |

## Company Blogs & Newsletters

| Source | Category |
|--------|----------|
| Sam Altman's blog | AI |
| OpenAI Blog | AI |
| Anthropic Blog | AI |
| NVIDIA Blog | Tech |
| Google AI Blog | AI |
| Microsoft AI Blog | AI |
| Meta AI Blog | AI |

People are searched via Google News RSS with `when:3d` filter (last 3 days). Blogs are fetched directly via RSS. Max 8 items per source.

## Output Fields

| Field | Description |
|-------|-------------|
| `author` | Person/org name |
| `handle` | Social media handle |
| `category` | ai, tech, or politics |
| `platform` | rss or blog |
| `title` | Headline |
| `link` | Article URL |
| `pubDate` | Publication date |
| `snippet` | Brief excerpt (max 300 chars) |
