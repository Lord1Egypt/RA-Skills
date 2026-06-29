# axiom-sql-formatter

> SQL formatter — uppercase keywords, line breaks, proper indentation.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

```
select id,name,email from users where active=true and created_at>'2024-01-01' order by created_at desc limit 100
```

Devient :

```sql
SELECT id,
  name,
  email
FROM users
WHERE active = TRUE
  AND created_at > '2024-01-01'
ORDER BY created_at DESC
LIMIT 100
```

**axiom-sql-formatter** : uppercase keywords, line breaks, indentation.

## 🚀 Usage

```bash
# Inline
python3 axiom_sql_formatter.py "select id, name from users where active = true"

# From file
python3 axiom_sql_formatter.py --file query.sql
```

## 🧪 Tests

11 tests passent.

## ⚠️ Limitations

- Pas de CTE récursifs
- Pas de window functions avancées
- Pas multi-statement

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.02/use |
