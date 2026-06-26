# Baseline Freeze (refactor/structured-v2.4)

Date: 2026-03-02 (Asia/Shanghai)
Branch: `refactor/structured-v2.4`

## 1) CLI help baseline

Command:

```bash
python3 load_character.py --help
```

Output:

```text
usage: load_character.py [-h] [--anime ANIME] [--output OUTPUT] [--info]
                         [--force] [--select SELECT]
                         name

Anime Character Loader v2.3 - Multi-source character data with validation

positional arguments:
  name                  Character name (EN/JP/CN)

optional arguments:
  -h, --help            show this help message and exit
  --anime ANIME, -a ANIME
                        Anime/manga name hint for disambiguation
  --output OUTPUT, -o OUTPUT
                        Output directory
  --info, -i            Show info only, don't generate
  --force, -f           Force generation even with low confidence
  --select SELECT, -s SELECT
                        Select specific match by index (when multiple found)
```

## 2) Key path command examples

```bash
# basic
python3 load_character.py "Kasumigaoka Utaha"

# with disambiguation hint
python3 load_character.py "Sakura" --anime "Fate"

# explicit select
python3 load_character.py "Sakura" --anime "Fate" --select 1

# info only
python3 load_character.py "加藤惠" --info
```

Note: examples are frozen from current README/SKILL behavior descriptions; not all were re-executed in this freeze step.
