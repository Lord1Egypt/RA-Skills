# 🎬 CC — FactSage Video Creation Manual

## 🔥 Kom godt i gang

```bash
# 1. Gå til factsage mappen
cd /home/openclaw/.openclaw/workspace/projects/factsage

# 2. Se hvilke scripts der er klar
ls scripts/

# 3. Vælg en video og kør (eksempel: House of Wisdom = #9)
python3 produce_with_manim.py 9

# 4. Find færdig video
ls output/cc-09-*.mp4

# 5. Upload via YouTube/TikTok
```

## 📜 FactSage Scripts

| # | Titel | Kørsel |
|---|-------|--------|
| 1 | Coffee ☕ | `python3 produce_with_manim.py 1` |
| 2 | University 🎓 | `python3 produce_with_manim.py 2` |
| 3 | Hospitals 🏥 | `python3 produce_with_manim.py 3` |
| 4 | Stars ⭐ | `python3 produce_with_manim.py 4` |
| 5 | Flying Machine 🛩️ | `python3 produce_with_manim.py 5` |
| 6 | Zero 0️⃣ | `python3 produce_with_manim.py 6` |
| 7 | Salahuddin ⚔️ | `python3 produce_with_manim.py 7` |
| 8 | Islamic Sicily 🌴 | `python3 produce_with_manim.py 8` |
| 9 | House of Wisdom 📚 | `python3 produce_with_manim.py 9` |

## 🚀 Tips

- Kør med `--quick` for hurtigere rendering (lavere kvalitet)
- Alle videoer har voiceover (Edge TTS)
- Rediger prompts i `animation_configs.py`
- Har du brug for hjælp? Sig til Jarvis! 🧠
