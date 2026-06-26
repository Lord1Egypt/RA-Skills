---
name: cine-cog
description: "AI cinematic video production powered by CellCog. Short films, music videos, brand films, widescreen cinematics. Consistent characters, cinematic lighting, visual storytelling — grand compositions from a single prompt."
metadata:
  openclaw:
    emoji: "🎬"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Cine Cog - Grand Cinema, Accessible to Everyone

**If you can imagine it, CellCog can film it.**

The grandest cinematics were locked behind million-dollar production budgets — epic compositions, consistent characters across scenes, cinematic lighting, sweeping narratives. For the first time, AI makes all of this accessible from a single prompt.

CellCog's mission with Cine-cog: **make the grandest visual storytelling available to everyone.** Character-consistent widescreen cinematics, generated from imagination, not budgets.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```


---

## What Makes Cine-cog Different

### Full Production Pipeline

From a single prompt, CellCog handles the entire cinematic pipeline:

1. **Script & storyboard** — Deep reasoning breaks your vision into scenes, shots, and narrative beats
2. **Character design** — Creates characters that stay consistent across every frame
3. **Scene generation** — Widescreen (16:9) frames with cinematic composition, lighting, and depth
4. **Animation** — Brings static frames to life with motion, camera movement, and lipsync
5. **Sound design** — Original score, voiceover, and sound effects
6. **Post-production** — Automatic editing, scene transitions, and final render

### What Previously Cost Millions

| Traditional Production | Cine-cog |
|----------------------|----------|
| Concept artists, storyboard artists | One prompt |
| Character designers ensuring consistency | Automatic across all scenes |
| Camera crews, lighting rigs | AI cinematography |
| Composers, sound engineers | Generated score + effects |
| Weeks of post-production | Automatic editing and rendering |
| Budget: $100K - $10M+ | Budget: One CellCog request |

---

## What Cinematics You Can Create

### Epic Narrative Films

Grand visual storytelling:

- **Fantasy Epics**: "Create a 3-minute cinematic: a lone knight approaches a dragon's lair at sunset"
- **Sci-Fi Visions**: "Film a 2-minute sequence: humanity's first steps on Mars, cinematic widescreen"
- **Historical Drama**: "Create a cinematic recreation of an ancient Roman triumph"
- **Mythological**: "Film the story of Icarus — from workshop to flight to fall — in 90 seconds"

**Example prompt:**
> "Create a 2-minute cinematic film:
> 
> Story: A young astronaut sees Earth from space for the first time
> 
> Scene 1: Inside the spacecraft — nervous anticipation, checking instruments
> Scene 2: The hatch opens — light floods in
> Scene 3: The reveal — Earth in full glory through the viewport
> Scene 4: Close-up — tears floating in zero gravity, awe on their face
> 
> Style: Interstellar meets Gravity. Widescreen 16:9.
> Music: Orchestral, building from quiet wonder to overwhelming emotion.
> No dialogue — let the visuals speak."

### Brand Cinematics

Premium visual content for brands:

- **Product Films**: "Create a 60-second cinematic product reveal for a luxury watch"
- **Brand Stories**: "Film a 2-minute origin story for our coffee brand — from bean to cup"
- **Launch Videos**: "Create a cinematic launch trailer for our new app"
- **Corporate Films**: "Film a 90-second cinematic company vision piece"

**Example prompt:**
> "Create a 90-second cinematic brand film:
> 
> Brand: A sustainable fashion company
> Story: Follow a garment from organic cotton field → artisan workshop → confident person wearing it in the city
> 
> Cinematography: Wide establishing shots of nature, intimate close-ups of craftsmanship, urban energy for the finale
> Color grade: Warm, earthy tones for nature → rich, confident tones for city
> Music: Acoustic guitar building to modern electronic
> 
> End with logo and tagline: 'Worn with purpose.'"

### Music Videos

Visual storytelling set to music:

- **Concept Videos**: "Create a music video with a surreal dreamscape narrative"
- **Performance Videos**: "Film a cinematic performance in an epic location"
- **Lyric Videos**: "Create a cinematic lyric video with visual storytelling"
- **Visualizers**: "Generate an atmospheric visual accompaniment for this track"

### Short Films

Complete narrative filmmaking:

- **Drama**: "Create a 3-minute short film about a father and daughter reconnecting"
- **Thriller**: "Film a 2-minute suspense sequence in an abandoned building"
- **Comedy**: "Create a 90-second comedy sketch with cinematic production value"
- **Experimental**: "Film an abstract visual poem about the passage of time"

---

## Cinematic Styles

| Style | Characteristics | Reference |
|-------|-----------------|-----------|
| **Epic/Grand** | Sweeping landscapes, orchestral score, wide shots | Lord of the Rings, Dune |
| **Intimate** | Close-ups, natural light, subtle emotion | Moonlight, Lost in Translation |
| **Noir** | High contrast, shadows, moody | Blade Runner, Sin City |
| **Naturalistic** | Golden hour, flowing camera, poetic | Terrence Malick, Studio Ghibli |
| **Hyper-stylized** | Bold colors, symmetry, precise framing | Wes Anderson, Wong Kar-wai |
| **Documentary** | Observational, raw, authentic | Planet Earth, Free Solo |

---

## Cinematic Specs

| Format | Dimensions | Best For |
|--------|------------|----------|
| **Widescreen** | 1920×1080 (16:9) | Standard cinematic |
| **Ultra-wide** | 2560×1080 (21:9) | Epic scope, letterbox feel |
| **Vertical** | 1080×1920 (9:16) | Reels/TikTok cinematics |
| **Square** | 1080×1080 (1:1) | Social media |

**Widescreen (16:9) is the default and recommended format** for cinematic content.

---

## Chat Mode for Cinematics

| Scenario | Recommended Mode |
|----------|------------------|
| Short clips, single scenes, thumbnails | `"agent"` |
| Full narrative films, multi-scene cinematics, brand films | `"agent team"` |

**Use `"agent team"` for most cinematic work.** Grand cinematics benefit from deep creative deliberation — storyboarding, character consistency, narrative flow, and production design all improve with multiple reasoning passes.

**Use `"agent"` for quick visual assets** — individual cinematic frames, thumbnails, or single short scenes.

---

## Example Prompts

**Grand cinematic:**
> "Create a 3-minute cinematic short film:
> 
> Title: 'The Last Library'
> Concept: In a post-apocalyptic world, a child discovers the last remaining library
> 
> Scenes:
> 1. Desolate landscape — child walking through ruins (30 sec)
> 2. Discovery — a door hidden behind rubble, light seeping through (20 sec)
> 3. The reveal — vast library interior, books everywhere, dust particles in light beams (30 sec)
> 4. Wonder — child touching books, opening one, illustrations come to life (40 sec)
> 5. Hope — child carries a book outside, sits and reads as sun sets (30 sec)
> 
> Style: Children of Men meets Studio Ghibli
> Music: Piano and strings, melancholic to hopeful
> No dialogue."

**Product cinematic:**
> "Create a 45-second cinematic product film for wireless headphones:
> 
> Open: Extreme macro of the headphone surface, light reflecting
> Build: Person puts them on in a busy city — the world goes quiet
> Showcase: Music fills the frame — visualize the audio quality cinematically
> Close: Product shot, floating, clean background
> 
> Cinematography: Macro lens → wide → intimate → product
> Color grade: Cool urban → warm personal → clean product
> Music: Something that makes you FEEL the audio quality"

**Short film:**
> "Create a 2-minute cinematic short:
> 
> Story: An old man sits alone at a café, looking at an empty chair across from him. 
> Through subtle flashbacks, we see decades of conversations at that same table.
> End: A young couple sits down at the next table, beginning their own story.
> 
> Style: Wong Kar-wai color palette, intimate framing
> Music: Solo piano, gentle
> Let the visuals and music tell the story — minimal or no dialogue."

---

## ⚠️ Important — Cinematic Video Generation Expectations

Long-form cinematic AI video production is at the absolute frontier of what's possible. While some users generate stunning, cinematic videos that are ready for production use, others may spend significant credits and still not achieve a usable result. Even spending thousands of credits does not guarantee a satisfactory outcome — this is the nature of where AI video technology stands today.

There is a real learning curve to generating cinematic videos with CellCog. It takes time, money, and patience. Your prompting skill, the complexity of your creative vision, and how well the foundation models perform on your specific request all play a role. Results improve as you develop intuition for what works, but we want to be upfront: cinematic video generation is inherently unpredictable, and there is always a risk that the output may not meet your expectations.

---

## Tips for Better Cinematics

1. **Think in scenes, not descriptions**: Break your vision into shots. "Wide establishing → medium → close-up" gives CellCog clear cinematic language.

2. **Reference real films**: "Blade Runner lighting" or "Wes Anderson framing" communicates more than paragraphs of description.

3. **Specify emotion, not just action**: "She looks out the window" is flat. "She looks out the window — longing, resignation, the smallest hint of hope" gives CellCog the emotional palette.

4. **Music direction matters**: The score transforms everything. Specify mood, instruments, and arc: "Builds from quiet uncertainty to confident resolution."

5. **Let silence work**: Not every scene needs dialogue. Some of the most powerful cinema is purely visual.

6. **Trust widescreen**: 16:9 is your default. It's how cinema is meant to be experienced.

---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
