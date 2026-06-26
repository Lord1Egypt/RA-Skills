# brouter 🚴

Generate **GPX bike routes** using the public [brouter.de](https://brouter.de) routing service.

This OpenClaw skill takes a start and end point plus a routing profile, calls brouter.de via `index.js`, and produces a GPX track file you can download or use in your navigation app.

## What This Skill Does

- Converts user intent ("bike route from A to B") into a **brouter.de** request
- Uses a **routing profile** that matches the user's preferences (fast, quiet, safe, road bike, etc.)
- Writes the resulting GPX file into the local `routes/` folder
- Returns the path/filename so you can share or download the GPX

Use this skill whenever the user wants a **bike route as a GPX file** between two places.

## Usage

### Natural-Language Triggers

You can call this skill from high-level prompts such as:

- "Create a GPX for a bike route from Prenzlauer Berg to Kreuzberg (profile: trekking)."
- "Give me a quiet route from Prenzlauer Berg to Kreuzberg as a GPX."
- "I need a fast bike route from Berlin Hauptbahnhof to Alexanderplatz as a GPX file."

## File Structure

```text
brouter/
├── SKILL.md     # High-level usage guidance (this skill spec)
├── README.md    # Practical docs for humans and agents (this file)
├── index.js     # Implementation that calls brouter.de and writes GPX files
├── routes/      # Generated GPX routes
└── .gitignore   # Ignores generated routes and node artifacts
```


Built for cyclists who want real, navigable GPX routes — not just a textual description.
