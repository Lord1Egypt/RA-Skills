"""
Pre-cache a demo story with all audio narrations + images stored in Turso.
Run once to seed the demo library with instant-playback stories.
"""
import os, json, base64, httpx, sys

ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
TURSO_URL = "https://your-db.turso.io"
TURSO_TOKEN = os.environ["TURSO_AUTH_TOKEN"]

HEADERS_TURSO = {"Authorization": f"Bearer {TURSO_TOKEN}", "Content-Type": "application/json"}

def turso_exec(sql, params=None):
    body = {"statements": [{"q": sql, "params": params or []}]}
    r = httpx.post(TURSO_URL, headers=HEADERS_TURSO, json=body, timeout=30)
    return r.json()

def generate_story(child_name, language, prompt):
    from mistralai import Mistral
    client = Mistral(api_key=MISTRAL_API_KEY)
    lang_names = {"en":"English","fr":"French","ja":"Japanese","hi":"Hindi","es":"Spanish"}
    lang_name = lang_names.get(language, "English")

    resp = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": f"""You are Anansi 🕷️, the master storyteller. Create a magical bedtime story for {child_name}.
Write in {lang_name}. 4-6 scenes, 2-3 sentences each. Gentle bedtime tone. End with child falling asleep.
Return JSON: {{"title": "...", "scenes": ["scene1", "scene2", ...], "mood": "calming|magical"}}"""},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(resp.choices[0].message.content.strip())

def generate_audio(text, voice_id="FGY2WhTYpPnrIDTdsKH5"):
    """Generate TTS audio, return base64 mp3"""
    r = httpx.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"},
        json={"text": text, "model_id": "eleven_multilingual_v2",
              "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}},
        timeout=30
    )
    if r.status_code != 200:
        print(f"  TTS error: {r.status_code} {r.text[:200]}")
        return None
    return base64.b64encode(r.content).decode()

def generate_sfx(prompt, duration=5.0):
    """Generate SFX, return base64 mp3"""
    r = httpx.post(
        "https://api.elevenlabs.io/v1/sound-generation",
        headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"},
        json={"text": prompt, "duration_seconds": duration},
        timeout=60
    )
    if r.status_code != 200:
        print(f"  SFX error: {r.status_code} {r.text[:200]}")
        return None
    return base64.b64encode(r.content).decode()

def generate_image(prompt, scene_num):
    """Generate image via Gemini Nano Banana Pro, return base64 png"""
    import google.generativeai as genai
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        print(f"  No GEMINI_API_KEY, skipping image for scene {scene_num}")
        return None
    genai.configure(api_key=gemini_key)
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(
            f"Children's book illustration, dreamy watercolor style: {prompt}",
            generation_config={"response_mime_type": "image/png"}
        )
        if response.parts and hasattr(response.parts[0], 'inline_data'):
            return base64.b64encode(response.parts[0].inline_data.data).decode()
    except Exception as e:
        print(f"  Image gen error: {e}")
    return None

# === DEMO STORIES TO PRE-CACHE ===
demos = [
    {
        "child_name": "Sophie",
        "language": "fr",
        "prompt": "Sophie loves whales and clouds. She barely hears French at school in Sydney. Tell her a magical bedtime story in French about cloud whales so she falls asleep hearing the words that feel like home.",
        "voice_id": "FGY2WhTYpPnrIDTdsKH5",  # Laura - warm female
        "sfx_mood": "gentle ocean waves with soft whale songs"
    },
]

for demo in demos:
    print(f"\n🕷️ Generating story for {demo['child_name']} ({demo['language']})...")
    story = generate_story(demo["child_name"], demo["language"], demo["prompt"])
    print(f"  Title: {story['title']}")
    print(f"  Scenes: {len(story['scenes'])}")

    # Generate audio for each scene
    audio_cache = {}
    for i, scene in enumerate(story["scenes"]):
        print(f"  🎙️ Narrating scene {i+1}/{len(story['scenes'])}...")
        audio_b64 = generate_audio(scene, demo["voice_id"])
        if audio_b64:
            audio_cache[str(i)] = audio_b64
            print(f"    ✅ {len(audio_b64)//1024}KB audio cached")

    # Generate ambient SFX
    print(f"  🎵 Generating ambient SFX...")
    sfx_b64 = generate_sfx(demo["sfx_mood"], 10.0)
    if sfx_b64:
        audio_cache["sfx"] = sfx_b64
        print(f"    ✅ {len(sfx_b64)//1024}KB SFX cached")

    # Generate lullaby
    print(f"  🎶 Generating lullaby...")
    lullaby_b64 = generate_sfx("Gentle soothing lullaby music box melody for bedtime, soft and calming", 15.0)
    if lullaby_b64:
        audio_cache["lullaby"] = lullaby_b64
        print(f"    ✅ {len(lullaby_b64)//1024}KB lullaby cached")

    # Save to Turso
    content_json = json.dumps(story, ensure_ascii=False)
    audio_json = json.dumps(audio_cache)

    sql = "INSERT INTO stories (title, content, voice_id, child_name, language, audio_cache) VALUES (?, ?, ?, ?, ?, ?)"
    turso_exec(sql, [story["title"], content_json, demo["voice_id"], demo["child_name"], demo["language"], audio_json])
    print(f"  💾 Saved to Turso with {len(audio_cache)} cached audio tracks")

print("\n✅ Demo stories pre-cached!")
