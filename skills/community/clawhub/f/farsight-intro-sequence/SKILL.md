---
name: "farsight-intro-sequence"
description: "Generate 100% original Farsight commercial video intros by analyzing structural elements of inspiration videos while strictly avoiding copyright infringement."
---

# SKILL: Farsight Commercial Intro Sequence Generation

## CORE PRINCIPLES & HARDLINE SAFETY RULES
1. **ZERO COPYRIGHT INFRINGEMENT:** This workflow is for generating COMMERCIAL products. You are strictly forbidden from incorporating any specific IP, names, credit text, character designs, or unique identifying elements from the inspiration material. 
2. **ORIGINALITY:** Every generated asset must be 100% original. The inspiration video is ONLY to be studied for its structural mechanics: movement of subjects, scene transitions (clipping), cinematography, pacing, framing, and overall vibe.
3. **NO HALLUCINATED TEXT:** When generating images, do not allow the AI to bake in hallucinated or spoofed text (like fake actor names or movie titles) from the inspiration piece. 
4. **EXPLICIT ENGINE CONFIRMATION:** Tool availability changes. You must ALWAYS ask the user which image generation engine and which video generation engine they want to use for the current run before generating media.

## PHASE 0: Context Gathering & File Organization
Before doing any analysis or generation, you must ask the user for and establish the following:
1. **Project Location:** Ask for the target directory where all files should be saved.
2. **Context Documents:** Ask for the location of the Target Information document and the Remote Viewer transcripts. Read these to understand the blind data and lore of the session.
3. **Inspiration Link:** The YouTube link for the video to study.
4. **Creative Direction:** Ask the user for the specific art style, the desired plot of the introduction sequence, and the appearance of the characters (since everything will be 100% different from the inspiration).
5. **Tool Selection:** Ask which Image Generation engine (e.g. standard Gemini, default OpenAI, etc.) and Video Generation engine (e.g. veo3, wavespeed, etc.) will be used for this project.

**File Setup:**
Once the location is confirmed, create the exact directory structure:
- `[Target_Directory]/AI Music Video/inspiration/`
- `[Target_Directory]/AI Music Video/inspiration/frames/`
- `[Target_Directory]/AI Music Video/Generated_Frames/`
- `[Target_Directory]/AI Music Video/[Chosen_Video_Engine_Name]/` (e.g., veo3, wavespeed)

## PHASE 1: Cinematographic Analysis (The "No Copyright" Zone)
1. Download the inspiration YouTube video to the `inspiration/` folder using `youtube-dl` or `yt-dlp` (via `exec`).
2. Extract frames (e.g., 1 frame per second) using `ffmpeg` into the `inspiration/frames/` folder.
   - Example command: `ffmpeg -i video.mp4 -vf fps=1 inspiration/frames/frame_%04d.png`
3. Analyze the frames purely for mechanics:
   - How does the camera move?
   - How do the scenes clip from one to the next?
   - How are subjects framed and lit?
4. **WARNING:** Strip all source identity from this analysis. Do not mention the original characters, names, or text. Create a sterile "structural map" of the video.

## PHASE 2: Prompt Engineering & Image Generation
1. Synthesize the context: Take the structural map from Phase 1 and merge it with the Target Information, Remote Viewer transcripts, requested art style, plot, and character descriptions from Phase 0.
2. Draft a detailed, second-by-second prompt report sequence. Ensure the plot order flows logically based on the user's instructions.
3. Present the prompt report to the user for approval. 
4. Upon approval, generate the images using the explicitly chosen engine via `image_generate`. Instruct the model to avoid white borders and ensure no unauthorized text is generated.
5. Save all approved image plates to the `Generated_Frames/` folder.

## PHASE 3: Animation & Finalization
1. Ask the user: "Do you want to animate this batch of images into video clips?"
2. If yes, confirm the settings and use the Video Generation engine explicitly chosen in Phase 0 via `video_generate` or via specialized tool commands.
3. Save the resulting video clips in the designated video folder (e.g., `veo3/` or `wavespeed/`).
4. Present final assets and await further instructions.
