# Song Library Management

## Adding Songs

Index individual songs:
```bash
node scripts/lyric-engine.js index "Artist Name" "Track Title"
```

Batch-index the starter library (30 songs across English/Spanish):
```bash
node scripts/lyric-engine.js batch-index
```

## Starter Library

The batch-index includes these genres/moods:

| Artist | Track | Mood/Use |
|--------|-------|----------|
| Eminem | Lose Yourself | Motivation, urgency, seizing the moment |
| Daft Punk | Giorgio by Moroder | Freedom, creativity, origin story |
| John Lennon | Imagine | Hope, peace, dreaming |
| Radiohead | Creep | Vulnerability, not belonging |
| Depeche Mode | Personal Jesus | Faith, reaching out |
| Jeff Buckley | Hallelujah | Sacred moments, bittersweet beauty |
| The Doors | Break on Through | Energy, celebration, breaking barriers |
| The Doors | Riders on the Storm | Danger, mystery, warning |
| Vicente Fernández | El Rey | Pride, defiance, Mexican identity |
| Q Lazzarus | Goodbye Horses | Eerie farewell, transcendence |
| Gustavo Cerati | Crimen | Longing, loss, Argentine rock |
| Natalia Lafourcade | Hasta la Raíz | Roots, devotion, staying |
| Carla Morrison | Disfruto | Love, commitment, loyalty |
| Mon Laferte | Tu Falta De Querer | Heartbreak, still loving |
| Zoé | Soñé | Dreams, revival |
| Soda Stereo | De Música Ligera | Lightness, classic rock en español |
| Café Tacvba | Eres | Love declaration, "here I am" |
| Caifanes | La Negra Tomasa | Joy, dance, party |
| Maldita Vecindad | Pachuco | Cultural pride, swagger |
| Molotov | Frijolero | Defiance, border politics |
| Pink Floyd | Comfortably Numb | Numbness, detachment, comfort |
| Pink Floyd | Wish You Were Here | Missing someone, nostalgia |
| Led Zeppelin | Stairway to Heaven | Journey, wisdom, epic build |
| Queen | Bohemian Rhapsody | Drama, existential crisis, opera |
| David Bowie | Heroes | Heroism, transcendence, love |
| Nirvana | Come As You Are | Acceptance, grunge authenticity |
| Bob Marley | Redemption Song | Freedom, empowerment |
| Funkadelic | Maggot Brain | Raw emotion (instrumental) |
| Kavinsky | Nightcall | Noir, night drive, synthwave |
| M83 | Midnight City | Night energy, euphoria |

## How Lyrics Are Sourced

1. **LRCLIB** (lrclib.net) — Free synced lyrics API, provides millisecond timestamps
2. **Spotify Search** — Matches to Spotify URIs for playback
3. Lyrics are stored in `lyric-index.json` with line-level timestamps

## Index Structure

Each indexed line contains:
- `id`: `artist::track::lineNumber`
- `text` / `textLower`: The lyric line
- `start_ms` / `end_ms`: Playback window
- `uri`: Spotify track URI
- `artist` / `track`: Display info
