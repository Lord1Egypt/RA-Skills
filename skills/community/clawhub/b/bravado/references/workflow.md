# Bravado production workflow

## 1. Source and evidence

Accept a running product URL, GitHub repository, or supplied resume/portfolio. With a document, extract source facts and distinguish employment, projects, prototypes, and aspirations; choose scenes that demonstrate the person’s actual work. Follow a repo's homepage or deployment link when available. Record the exact source URL, access date, current features, audience, visual identity, logo, and factual claims. Capture current desktop and mobile references. A repo-only product may lack a brand; create a design direction explicitly marked as a proposal. Never infer launch status, customer counts, or metrics from aspirational README copy.

Run `python inspect_source.py URL --out output/source-notes.json` as a first pass. The agent still has to inspect the UI, graphics, and product state through available browsing or source tools. Ask for a missing private asset only when it materially blocks faithful production; otherwise create a reviewable treatment.

## 2. Story and motion treatment

Build a 31-second arc around the actual product:

| Window | Narrative job | Motion job |
| --- | --- | --- |
| 0–3 s | Hook | Brand signal and first visual motif |
| 3–7.5 s | Problem | Accumulation, delay, friction, or contrast |
| 7.5–12 s | Shift | Transform the old state into the new one |
| 12–17.5 s | Mechanism | One legible model or live-style demonstration |
| 17.5–23 s | Flow | Show actors, data, objects, or outcomes in motion |
| 23–27 s | Proof | Records, results, verifiable output, or concise evidence |
| 27–31 s | Brand | Name, proposition, and clear call to action |

Write each headline in one or two short lines. Pick one literal graphic metaphor that the product supports: a route, flow, orbit, stack, queue, network, chart, timeline, or transformation. Define the motion's cause and effect, not just entrance effects. Build a beat sheet with the start/end of each action and the matching sound cue. Source footage and logos must have appropriate rights.

## 3. Build

Copy and adapt `projects/cadence.json`. Use the actual palette/type from the source when possible. Replace Cadence-specific graphical scenes in `render.py` when the product needs another visual model. The seven time windows are the starter grammar; adapt them deliberately when the story needs a different structure, updating visual timing, audio cues, review samples, and export expectations together. Keep logos as actual assets or faithful vectors; avoid using a text monogram when a supplied logo is available.

Run `python render.py --brief projects/your-project.json --validate-only` before rendering with the starter. Custom project renderers need their own input checks. Render storyboards first. The starter also saves `boundary-*.jpg` at the last old-scene frame, exact cut, mid-wipe, settled new scene, and final video frame. Check headline hierarchy, contrast, crop safety, continuous motion, graph semantics, and readability on a phone. Review transitions at the exact cut frames. After changes, render the full MP4. Listen to headphones: rhythmic bed, transients, stereo balance, ending, and silence between accents. The synthesized score in `make_audio` is a starting point; alter frequencies and hit times to match the visual beats. Audio from a reference video is never copied into the output.

## 4. Verify and deliver

Run `python verify_export.py output/your-film.mp4` to check duration, 1920×1080 resolution, 30 fps, H.264 video, AAC stereo, and decode both streams to the end. For intentional format changes, pass the corresponding width, height, fps, and duration options. Watch the export, not only preview frames. Confirm copy against the source, product availability, the correct URL/CTA, metric arithmetic, and any illustrative-data labeling. Deliver the MP4 and an editable project with the source brief, code, assets, and soundtrack. State any evidence gaps precisely.

The repository workflow `.github/workflows/render.yml` runs the renderer and uploads reviewable artifacts. It is a render gate, not editorial approval. A human or agent must inspect the video before publication.
