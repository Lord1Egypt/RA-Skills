---
name: codex-profile-failover
description: OpenClaw içinde birden fazla openai-codex OAuth profili varken otomatik ve manuel profil taklası sağlar. Aktif profilin kalan kullanım oranı yüzde 10 gibi bir eşik altına düştüğünde, 401 veya eksik token gibi usage/auth hataları oluştuğunda ya da operatör manuel tetikleme istediğinde session `authProfileOverride` alanını daha sağlıklı profile geçirmen gerektiğinde kullan.
---

# Codex Profile Failover

Bu skill, OpenClaw auth profilleri üstüne hafif bir Codex profil takla katmanı ekler.

## Bu skill ne sağlar

- Aktif profili canlı usage ile izleyen watchdog
- Cron veya tek seferlik kullanım için threshold guard
- Operatörün elle çalıştırabileceği manuel tetikleme scripti
- Session için doğrudan `authProfileOverride` yazan helper
- Genel amaçlı config şablonları ve kurulum notları

## Temel davranış

Bir profil şu koşullardan biri varsa değiştirilmeye aday sayılır:

- efektif kalan kullanım oranı eşik değerin altına düşmüşse
- usage kontrolü auth veya transport hatası döndürüyorsa ve `switchOnUsageError` açıksa
- token yerelde eksik veya süresi geçmiş görünüyorsa

Geçişte, eşik üstünde kalan en sağlıklı alternatif profil tercih edilir. Tüm adaylarda canlı usage okunamıyorsa, yerelde hâlâ geçerli görünen token için sınırlı bir fallback uygulanabilir.

## Dahili scriptler

- `scripts/codex_profile_runtime.py` auth profile okuma ve canlı usage yardımcıları
- `scripts/codex_profile_watchdog.py` uzun süreli arka plan watchdog
- `scripts/codex_profile_threshold_guard.py` tek seferlik eşik kontrolü
- `scripts/assign_codex_profile_to_session.py` session `authProfileOverride` alanını yazar
- `scripts/trigger_profile_failover.py` operatör için manuel takla tetikleyicisi
- `scripts/install_codex_profile_failover.py` hedef workspace içine generic config yazar

## Hızlı başlangıç

1. `references/setup.md` dosyasını oku.
2. Installer helper'ı çalıştır veya örnek configleri elle kopyala.
3. Önce dry-run ile kontrol et.
4. Sonra bir kez apply ile gerçek geçiş dene.
5. Her şey doğruysa watchdog'u arka planda başlat.

## Önerilen kurulum akışı

### Configleri yaz

```bash
python3 scripts/install_codex_profile_failover.py --workspace /path/to/workspace --session-key agent:main:main
```

### Dry-run kontrolü

```bash
python3 scripts/codex_profile_threshold_guard.py --config /path/to/workspace/config/codex-profile-rotation.json --json
```

### Gerçek bir geçiş uygula

```bash
python3 scripts/codex_profile_threshold_guard.py --config /path/to/workspace/config/codex-profile-rotation.json --apply --json
```

### Watchdog'u başlat

```bash
nohup python3 scripts/codex_profile_watchdog.py --config /path/to/workspace/config/codex-profile-watchdog.json --apply >> /path/to/workspace/state/codex-profile-watchdog.log 2>&1 &
```

### Manuel tetikleme

```bash
python3 scripts/trigger_profile_failover.py --config /path/to/workspace/config/codex-profile-watchdog.json
```

## Tasarım kuralları

- Profil id'lerini sabit ve generic tut.
- Mümkünse email veya account başına tek profil yaklaşımını tercih et.
- Workspace snapshot mantığını otomatik yan etki değil, açık uyumluluk katmanı olarak tut.
- Skill içine kişisel email, user id veya kanal id koyma.
- Ortama özel değerleri scriptlerin içine gömme, kurulum sırasında yazılan configlerde tut.

## Önemli not

Bu skill, install edildiği anda tek başına tamamen aktif olmaz. Skill dosyalarını getirir, sonra installer helper ile config yazılması ve watchdog'un ayrıca başlatılması gerekir.

## Doğrulama listesi

- `auth-profiles.json` içinde birden fazla `openai-codex:*` profil var
- hedef session `sessions.json` içinde mevcut
- dry-run beklenen aktif profili ve adayı gösteriyor
- apply sonrası `authProfileOverride` ve `authProfileOverrideSource` yazılıyor
- event log ve backup dosyaları workspace state dizininde oluşuyor
- watchdog tekrar eden çalışmalarda sağlıklı kalıyor

## Referanslar

- Kurulum ve publish öncesi temizlik için `references/setup.md`
- Generic config örnekleri için `references/watchdog-config.example.json` ve `references/threshold-config.example.json`
