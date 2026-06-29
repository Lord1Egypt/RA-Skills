# axiom-url-canonicalizer

> URL normalizer for SEO and cache deduplication.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

`HTTP://Example.COM:80/Path/?b=2&a=1#frag` et `http://example.com/path?a=1&b=2` sont la **même** URL pour Google, mais deux chaînes différentes pour un cache naïf.

**axiom-url-canonicalizer** normalise : scheme lowercase, host lowercase, port par défaut retiré, query triée, fragment stripable, `/./` et `/../` résolus.

Cas d'usage :
- SEO (éviter duplicate content)
- Cache HTTP (réduire les misses)
- Détection de duplicate URLs
- Tracking param removal (`utm_*`, `fbclid`, etc.)

## 🚀 Usage

```bash
# Standard
python3 axiom_url_canonicalizer.py "HTTP://Example.COM:80/Path/?b=2&a=1#frag"
# Original:  HTTP://Example.COM:80/Path/?b=2&a=1#frag
# Canonical: http://example.com/Path/?a=1&b=2

# Strip tracking
python3 axiom_url_canonicalizer.py "https://shop.com/?a=1&utm_source=fb" --strip-tracking

# Force HTTPS
python3 axiom_url_canonicalizer.py "http://example.com/" --force-https

# JSON
python3 axiom_url_canonicalizer.py "https://example.com/path?q=1" --json
```

## 🧪 Tests

20 tests passent (0.005s).

## ⚠️ Limitations

- Pas de résolution DNS
- IDN/percent-encoding partiel
- Pas de support javascript: / mailto: / data: schemes

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.02/use |
