# Moving a Spotify playlist to Apple Music

`import_playlist.py` rebuilds a playlist from a CSV or a plain list. It previews first and only
creates the playlist when you add `--create`.

## 1. Get your playlist out of Spotify

Pick whichever is easier.

**A CSV export.** Third-party tools such as [Exportify](https://github.com/watsonbox/exportify) (not affiliated with
this project or with Spotify; its README links the hosted app) sign in to your Spotify account and save a
playlist as a CSV. Exportify's files have `Track Name`, `Artist Name(s)` and `ISRC` columns, which the
importer reads as they are. Check what any such tool asks permission for before you sign in.

**A plain list.** Copy the playlist out of the Spotify app and paste it into a text file, one
`Artist - Title` per line. Blank lines and lines starting with `#` are ignored:

```
Radiohead - Idioteque
Oasis - Wonderwall
```

## 2. Preview

```bash
python3 scripts/import_playlist.py my-playlist.csv
```

Nothing is written. You get counts and the list of tracks that will be added:

```json
{"counts": {"total": 4, "exact": 0, "fuzzy": 3, "unmatched": 1, "duplicates": 0}}
```

- **exact** — matched by ISRC (the recording's international code). Exportify's CSVs include it, so
  most tracks land here. If your file has no `ISRC` column, or a row's code is blank, that row falls
  back to the title + artist search below.
- **fuzzy** — matched by a strict title + artist search. "Wonderwall - Remastered" finds
  "Wonderwall"; the artist must match as well.
- **unmatched** — nothing in the Apple Music catalog fit well enough. These are listed, never
  guessed. Search for them by hand in Apple Music and add them afterwards.

You can try this with no account: `python3 scripts/demo.py run import_playlist.py
assets/sample-spotify-export.csv --storefront us` runs against the demo catalog. The sample has no
`ISRC` column on purpose, so it shows the title + artist path (the `fuzzy` count).

## 3. Create it

```bash
python3 scripts/import_playlist.py my-playlist.csv --create --name "From Spotify"
```

The playlist appears in your Apple Music library. If a playlist with that name already exists,
nothing is created and the command exits with an error; pick another name.

## Limits

- Up to 500 rows per file.
- Anything Apple Music does not carry (local files, podcasts, some regional releases) comes back
  as unmatched.
- Artists: when credits are separated by `;` only the first is used. Exportify separates them with
  commas (`Artist A, Artist B`), so the whole credit is kept; it still matches when Apple Music lists
  the same collaborators, but can come back unmatched if Apple Music orders them differently or
  credits only the main artist. This only matters for rows without an ISRC.
