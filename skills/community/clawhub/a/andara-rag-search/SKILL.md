---
name: andara-rag-search
description: Search the Andara Ionic RAG knowledge base (3,800+ records) for business intel, research, products, team, meetings, and any indexed content.
---

# Andara RAG Knowledge Search

Use this skill when you need to find information about:
- Team members, roles, responsibilities
- Products, pricing, supplier details
- Scientific research, water science, bioelectricity
- Business structure, equity, governance
- Meeting notes, action items, decisions
- CMS pages, content, topic clusters
- Orders, customers, revenue data
- Any business intelligence question

## How to Use

Run a PostgreSQL query against the `knowledge_base` table using the `bash` tool:

```bash
psql "$DATABASE_URL" \
  -c "SELECT content::text, source, data_type FROM knowledge_base WHERE content::text ILIKE '%SEARCH_TERM%' LIMIT 5;"
```

Replace `SEARCH_TERM` with the relevant keyword(s).

## Available Tables

### Core Data
| Table | Description | Key Columns |
|-------|-------------|-------------|
| `knowledge_base` | RAG chunks (3,800+) | `content`, `source`, `data_type` |
| `team_members` | Team roster (6 active) | `name`, `role`, `title`, `email`, `department`, `equity_percent` |
| `team_meetings` | Meeting notes (5) | `title`, `date`, `summary`, `key_insights`, `decisions` |
| `meeting_action_items` | Action items (32) | `title`, `assignee`, `status`, `priority`, `due_date` |
| `team_goals` | Company goals (4) | `title`, `status`, `target_date`, `progress_percent` |

### CMS & Commerce
| Table | Description | Key Columns |
|-------|-------------|-------------|
| `pages` | CMS pages (155) | `slug`, `title`, `content`, `zone`, `cluster_id`, `status` |
| `products` | Products (2) | `name`, `price_cents`, `description`, `sku` |
| `orders` | Orders (11) | `total`, `status`, `customer_name`, `created_at` |
| `customers` | Customers (10) | `name`, `email`, `created_at` |
| `clusters` | Topic clusters (20) | `name`, `slug`, `description` |

### Intelligence
| Table | Description |
|-------|-------------|
| `rag_memory_objects` | Learned lessons & policies |
| `science_articles` | Scientific content |
| `newsletter_subscribers` | Email subscribers |

## Example Queries

### Find team member info
```bash
psql "$DATABASE_URL" \
  -c "SELECT name, title, department, equity_percent FROM team_members WHERE is_active = true;"
```

### Search knowledge base
```bash
psql "$DATABASE_URL" \
  -c "SELECT LEFT(content::text, 300) as content, source FROM knowledge_base WHERE content::text ILIKE '%chris%' LIMIT 5;"
```

### Get CMS page content
```bash
psql "$DATABASE_URL" \
  -c "SELECT slug, title, zone FROM pages WHERE status = 'published' ORDER BY slug LIMIT 20;"
```

### Get revenue summary
```bash
psql "$DATABASE_URL" \
  -c "SELECT COUNT(*) as orders, SUM(total)/100.0 as revenue_eur, AVG(total)/100.0 as avg_order FROM orders;"
```

### Get meeting action items by person
```bash
psql "$DATABASE_URL" \
  -c "SELECT title, status, priority, due_date FROM meeting_action_items WHERE assignee ILIKE '%chris%';"
```

### Get page content by slug
```bash
psql "$DATABASE_URL" \
  -c "SELECT title, LEFT(content, 500) as content_preview FROM pages WHERE slug = '/ion/overview';"
```

## Rules
- Always use `LEFT(content::text, 300)` to truncate long content fields (content is jsonb, must cast to text)
- Default LIMIT to 5-10 results to keep responses concise
- Use `ILIKE` for case-insensitive text searches
- Never INSERT, UPDATE, or DELETE — read-only access only
- For questions about the website structure, query the `pages` table
- For scientific questions, search `knowledge_base` WHERE `data_type = 'research'` OR search `science_articles`
