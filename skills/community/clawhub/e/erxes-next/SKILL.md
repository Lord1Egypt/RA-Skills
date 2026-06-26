---
name: erxes
emoji: 🔌
description: >
  Manage contacts, companies, products, tags, documents, brands, automations,
  team members, and organization data on an erxes instance. Use when the user
  wants to view, create, update, or remove erxes data through GraphQL.
requires:
  - env: ERXES_BASE_URL
    description: "erxes gateway URL, for example https://your-subdomain.next.erxes.io/gateway or http://localhost:4000"
---

# erxes– Чадварууд

## Login

Use `scripts/login.sh` for authentication.

```bash
ERXES_BASE_URL=<url> ERXES_CLIENT_ID=${ERXES_CLIENT_ID:-erxes-local} bash scripts/login.sh
```

- `ERXES_BASE_URL` is required.
- `ERXES_CLIENT_ID` is optional. Default to `erxes-local`.
- Accept the URL in whatever form the user gives and normalize it to `ERXES_BASE_URL=<url>`.
- Do not explain OAuth internals unless the user asks.
- Do not ask the user to copy tokens manually.
- Do not store tokens in project files.
- The script opens the browser, waits for approval, and prints a session JSON payload to stdout.

Read [erxes-app-token-auth.md](./erxes-app-token-auth.md) only when you need the quick login reference.

## API calls

After login, use the returned session payload directly.

- Read `accessToken` from the login JSON response.
- Send `Authorization: Bearer <accessToken>` and `erxes-subdomain: <subdomain>` headers on GraphQL calls.
- If the access token expires during the current task, use the in-memory `refreshToken` to get a new access token.
- Do not write tokens to `.auth.json` or any other project file.
- Read [erxes-graphql-api.md](./erxes-graphql-api.md) only when you need query or mutation examples.

---

## Харилцагч

- Бүх харилцагчийн жагсаалт харах
- Нэр, имэйл, утсаар хайх
- Харилцагчийн дэлгэрэнгүй мэдээлэл харах
- Төрлөөр нь бүлэглэх (үйлчлүүлэгч / боломжит / зочин)
- Шинэ харилцагч нэмэх
- Харилцагчийн мэдээлэл засах
- Харилцагч устгах
- Давхардсан харилцагчийг нэгтгэх

## Бүтээгдэхүүн

- Бүтээгдэхүүний жагсаалт харах
- Нэг бүтээгдэхүүний дэлгэрэнгүй харах
- Шинэ бүтээгдэхүүн нэмэх
- Бүтээгдэхүүн засах, устгах, нэгтгэх
- Ангилал болон хэмжих нэгж удирдах

## Шошго

- Бүх шошго харах
- Шошго нэмэх, засах, устгах
- Харилцагч эсвэл бүтээгдэхүүнд шошго хавсаргах

## Баримт бичиг

- Баримт бичгийн жагсаалт харах
- Баримт бичиг нэмэх, засах, устгах

## Брэнд

- Брэндийн жагсаалт харах
- Брэнд нэмэх, засах, устгах

## Автоматжуулалт

- Бүх автоматжуулалтын жагсаалт харах
- Автоматжуулалт нэмэх, засах, идэвхжүүлэх, устгах

## Байгууллагын бүтэц

- Хэлтэс, салбар, нэгж, албан тушаалын бүтэц харах
- Хэлтэс, салбар, нэгж, тушаал нэмэх, засах, устгах

## Багийн гишүүд

- Гишүүдийн жагсаалт харах
- Шинэ гишүүн урих
- Гишүүний мэдээлэл засах
- Гишүүнийг идэвхгүй болгох

## References
- scripts/login.sh — Browser login helper
- erxes-app-token-auth.md — Quick login reference
- erxes-graphql-api.md — Үйлдлүүдийн техникийн лавлах
