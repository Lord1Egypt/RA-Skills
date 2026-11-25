#!/usr/bin/env python3
"""
demo.py — Try Apple Music DJ without an Apple Developer account or any tokens.

Runs the skill's real scripts against a local stand-in for the Apple Music API: a fictional
listener and a sample catalog of about 250 songs, served on 127.0.0.1 only for as long as the command runs.
Nothing is sent to Apple and nothing touches your Apple Music account. Demo data lives in
~/.apple-music-dj-demo/, apart from your real data.

Usage:
  python3 scripts/demo.py tour                    # a guided tour: taste profile, card, playlists
  python3 scripts/demo.py run <script> [args...]  # any skill script in demo mode
  python3 scripts/demo.py serve [--port 8765]     # just the mock API (for development)
  python3 scripts/demo.py reset                   # delete the demo data folder

In `run`, the word DEMO_PROFILE stands for the demo listener's taste profile:
  python3 scripts/demo.py run taste_card.py DEMO_PROFILE --format text
  python3 scripts/demo.py run strategy_engine.py --strategy similar --similar-to Radiohead --profile DEMO_PROFILE

The same server backs the end-to-end tests (tests/test_integration_mock_api.py), which assert on
every request it records. Response shapes follow Apple's documentation but are NOT verified
against the real service.
"""

import sys
if sys.version_info < (3, 11):
    sys.exit(
        f"ERROR: Python 3.11+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import contextlib
import os
import re
import shutil
import subprocess
from pathlib import Path
import json
import threading
import socketserver
from itertools import zip_longest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse


class LoopbackHTTPServer(ThreadingHTTPServer):
    """ThreadingHTTPServer without HTTPServer.server_bind's socket.getfqdn() reverse-DNS lookup.

    The server only binds 127.0.0.1, and on some macOS setups that lookup hangs ~35 s before failing.
    """

    def server_bind(self):
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]


# ── Fixed catalogs ───────────────────────────────────────────────
# Two catalogs behind one mock. SMALL_CATALOG is a dozen songs that the integration tests assert
# against, so it must stay put. DEMO_CATALOG is what demo mode and `demo.py serve` use: about 170
# songs, big enough that every strategy fills a playlist.

# id, name, artist id, genres, release date, album id, isrc [, track number]
SongRow = tuple


class Catalog:
    """The fictional world the mock serves: songs, albums, artists, and one listener's library."""

    def __init__(self, artists: dict[str, dict[str, Any]], songs: list[SongRow], albums: dict[str, tuple],
                 similar: dict[str, list[str]], *, content_ratings: dict[str, str], playlist_id: str,
                 playlist_name: str, playlist_songs: list[str], library_songs: list[str],
                 ratings: dict[str, int], recent_tracks: list[str], library_artists: list[str],
                 charts: list[str], recently_added_album: str, top_songs: int = 2, spread_top_songs: bool = False,
                 playlist_page_size: int = 100):
        self.artists, self.songs, self.albums, self.similar = artists, songs, albums, similar
        self.content_ratings = content_ratings
        self.playlist_id, self.playlist_name, self.playlist_songs = playlist_id, playlist_name, playlist_songs
        self.library_songs, self.ratings, self.recent_tracks = library_songs, ratings, recent_tracks
        self.library_artists, self.charts = library_artists, charts
        self.recently_added_album, self.top_songs = recently_added_album, top_songs
        self.spread_top_songs = spread_top_songs
        self.playlist_page_size = playlist_page_size  # Apple pages long playlists; tests shrink this

    def top_songs_for(self, aid: str) -> list[dict]:
        """An artist's top songs. SMALL_CATALOG keeps catalog order; DEMO_CATALOG takes one song from
        each album in turn, as a real artist's top songs span albums."""
        rows = [r for r in self.songs if r[2] == aid]
        if self.spread_top_songs:
            by_album: dict[str, list[SongRow]] = {}
            for r in rows:
                by_album.setdefault(r[5], []).append(r)
            rows = [r for group in zip_longest(*by_album.values()) for r in group if r]
        return [self.song(r[0]) for r in rows[:self.top_songs]]

    def song(self, sid: str) -> dict:
        row = next(r for r in self.songs if r[0] == sid)
        _, name, aid, genres, date, alb, isrc, *track = row
        rating = {"contentRating": self.content_ratings[sid]} if sid in self.content_ratings else {}
        return {
            "id": sid, "type": "songs",
            "attributes": {
                **rating,
                "name": name, "artistName": self.artists[aid]["name"], "genreNames": genres + ["Music"],
                "releaseDate": date, "albumName": self.albums[alb][0], "isrc": isrc,
                "trackNumber": track[0] if track else 1,
                "durationInMillis": 170_000 + int(sid[1:]) % 6 * 25_000,  # 2:50 to 4:55, varied but fixed
            },
            "relationships": {"artists": {"data": [{"id": aid, "type": "artists"}]},
                              "albums": {"data": [{"id": alb, "type": "albums"}]}},
        }

    def artist(self, aid: str) -> dict:
        a = self.artists[aid]
        return {"id": aid, "type": "artists", "attributes": {"name": a["name"], "genreNames": a["genres"]}}

    def album(self, alb_id: str) -> dict:
        name, aid, date = self.albums[alb_id]
        return {"id": alb_id, "type": "albums",
                "attributes": {"name": name, "artistName": self.artists[aid]["name"], "releaseDate": date,
                               "isSingle": False, "trackCount": sum(1 for r in self.songs if r[5] == alb_id),
                               "genreNames": self.artists[aid]["genres"]}}


SMALL_CATALOG = Catalog(
    artists={
        "a1": {"name": "Radiohead", "genres": ["Alternative", "Music"]},
        "a2": {"name": "Oasis", "genres": ["Rock", "Alternative", "Music"]},
        "a3": {"name": "Björk", "genres": ["Electronic", "Music"]},
        "a4": {"name": "Muse", "genres": ["Alternative", "Music"]},
    },
    songs=[
        ("s1", "Karma Police", "a1", ["Alternative"], "1997-05-21", "alb1", "GBAYE9700001"),
        ("s2", "Paranoid Android", "a1", ["Alternative"], "1997-05-21", "alb1", "GBAYE9700002"),
        ("s3", "Let Down", "a1", ["Alternative"], "1997-05-21", "alb1", "GBAYE9700003"),
        ("s4", "Idioteque", "a1", ["Alternative", "Electronic"], "2000-10-02", "alb2", "GBAYE0000004"),
        ("s5", "Everything In Its Right Place", "a1", ["Alternative"], "2000-10-02", "alb2", "GBAYE0000005"),
        ("s6", "Wonderwall", "a2", ["Rock"], "1995-10-02", "alb3", "GBAYE9500006"),
        ("s7", "Champagne Supernova", "a2", ["Rock"], "1995-10-02", "alb3", "GBAYE9500007"),
        ("s8", "Don't Look Back in Anger", "a2", ["Rock"], "1995-10-02", "alb3", "GBAYE9500008"),
        ("s9", "Starlight", "a4", ["Alternative"], "2006-06-19", "alb4", "GBAYE0600009"),
        ("s10", "Supermassive Black Hole", "a4", ["Alternative", "Rock"], "2006-06-19", "alb4", "GBAYE0600010"),
        ("s11", "Jóga", "a3", ["Electronic"], "1997-09-22", "alb5", "GBAYE9700011"),
        ("s12", "Bachelorette", "a3", ["Electronic"], "1997-09-22", "alb5", "GBAYE9700012"),
        ("s13", "Champagne Supernova", "a2", ["Rock"], "1995-10-02", "alb3", "GBAYE9500013"),  # the clean twin of s7
    ],
    albums={
        "alb1": ("OK Computer", "a1", "1997-05-21"),
        "alb2": ("Kid A", "a1", "2000-10-02"),
        "alb3": ("(What's the Story) Morning Glory?", "a2", "1995-10-02"),
        "alb4": ("Black Holes and Revelations", "a4", "2006-06-19"),
        "alb5": ("Homogenic", "a3", "1997-09-22"),
    },
    similar={"a1": ["a2", "a4"], "a2": ["a1"], "a3": ["a1"], "a4": ["a1", "a2"]},
    content_ratings={"s7": "explicit", "s12": "explicit", "s13": "clean"},  # s7 has a clean twin (s13); s12 has none
    playlist_id="pl.demo-alt-essentials", playlist_name="Alt Essentials", playlist_songs=[f"s{i}" for i in range(1, 14)],
    library_songs=["s1", "s4"], ratings={"s5": 1, "s11": -1}, recent_tracks=["s1", "s2", "s6"],
    library_artists=["a1", "a2"], charts=["s9", "s12"], recently_added_album="alb4",
)

# artist -> (name, genres); album -> (artist, title, release date, genres, track titles). Real albums
# and track lists; the listener and the library built from them are fictional.
_DEMO_ARTISTS = {
    "radiohead": ("Radiohead", ["Alternative"]), "oasis": ("Oasis", ["Rock", "Alternative"]),
    "muse": ("Muse", ["Alternative", "Rock"]), "bjork": ("Björk", ["Electronic"]),
    "daftpunk": ("Daft Punk", ["Electronic", "Dance"]), "portishead": ("Portishead", ["Electronic"]),
    "miles": ("Miles Davis", ["Jazz"]), "amy": ("Amy Winehouse", ["R&B/Soul"]),
    "floyd": ("Pink Floyd", ["Rock"]), "nirvana": ("Nirvana", ["Alternative", "Rock"]),
    "mac": ("Fleetwood Mac", ["Rock", "Pop"]), "mj": ("Michael Jackson", ["Pop", "R&B/Soul"]),
    "kendrick": ("Kendrick Lamar", ["Hip-Hop/Rap"]), "norah": ("Norah Jones", ["Jazz"]),
    "eno": ("Brian Eno", ["Ambient"]), "aphex": ("Aphex Twin", ["Electronic", "Ambient"]),
    "cash": ("Johnny Cash", ["Country"]), "foxes": ("Fleet Foxes", ["Folk"]),
    "dua": ("Dua Lipa", ["Pop", "Dance"]), "metallica": ("Metallica", ["Metal"]),
    "massive": ("Massive Attack", ["Electronic"]), "verve": ("The Verve", ["Alternative", "Rock"]),
    "pulp": ("Pulp", ["Alternative", "Rock"]), "blur": ("Blur", ["Alternative", "Rock"]),
    "beck": ("Beck", ["Alternative"]), "moby": ("Moby", ["Electronic"]),
}
_DEMO_ALBUMS = [
    ("radiohead", "OK Computer", "1997-05-21", ["Alternative"], [
        "Airbag", "Paranoid Android", "Subterranean Homesick Alien", "Exit Music (For a Film)", "Let Down",
        "Karma Police", "Fitter Happier", "Electioneering", "Climbing Up the Walls", "No Surprises", "Lucky",
        "The Tourist"]),
    ("radiohead", "Kid A", "2000-10-02", ["Alternative", "Electronic"], [
        "Everything In Its Right Place", "Kid A", "The National Anthem", "How to Disappear Completely",
        "Treefingers", "Optimistic", "In Limbo", "Idioteque", "Morning Bell", "Motion Picture Soundtrack"]),
    ("radiohead", "The Bends", "1995-03-13", ["Alternative"], [
        "Planet Telex", "The Bends", "High and Dry", "Fake Plastic Trees", "Bones", "(Nice Dream)", "Just",
        "My Iron Lung", "Bullet Proof..I Wish I Was", "Black Star", "Sulk", "Street Spirit (Fade Out)"]),
    ("radiohead", "In Rainbows", "2007-10-10", ["Alternative"], [
        "15 Step", "Bodysnatchers", "Nude", "Weird Fishes/Arpeggi", "All I Need", "Faust Arp", "Reckoner",
        "House of Cards", "Jigsaw Falling into Place", "Videotape"]),
    ("oasis", "(What's the Story) Morning Glory?", "1995-10-02", ["Rock"], [
        "Hello", "Roll with It", "Wonderwall", "Don't Look Back in Anger", "Hey Now!", "Some Might Say",
        "Cast No Shadow", "She's Electric", "Morning Glory", "Champagne Supernova"]),
    ("muse", "Origin of Symmetry", "2001-06-18", ["Alternative", "Rock"], [
        "New Born", "Bliss", "Space Dementia", "Hyper Music", "Plug In Baby", "Citizen Erased", "Micro Cuts",
        "Screenager", "Darkshines", "Feeling Good", "Megalomania"]),
    ("muse", "Black Holes and Revelations", "2006-06-19", ["Alternative", "Rock"], [
        "Take a Bow", "Starlight", "Supermassive Black Hole", "Map of the Problematique", "Soldier's Poem",
        "Invincible", "Assassin", "Exo-Politics", "City of Delusion", "Hoodoo", "Knights of Cydonia"]),
    ("bjork", "Post", "1995-06-13", ["Electronic"], [
        "Army of Me", "Hyperballad", "The Modern Things", "It's Oh So Quiet", "Enjoy", "You've Been Flirting Again",
        "Isobel", "Possibly Maybe", "I Miss You", "Cover Me", "Headphones"]),
    ("bjork", "Homogenic", "1997-09-22", ["Electronic"], [
        "Hunter", "Jóga", "Unravel", "Bachelorette", "All Neon Like", "5 Years", "Immature", "Alarm Call",
        "Pluto", "All Is Full of Love"]),
    ("daftpunk", "Discovery", "2001-03-12", ["Electronic", "Dance"], [
        "One More Time", "Aerodynamic", "Digital Love", "Harder, Better, Faster, Stronger", "Crescendolls",
        "Nightvision", "Superheroes", "High Life"]),
    ("portishead", "Dummy", "1994-08-22", ["Electronic"], [
        "Mysterons", "Sour Times", "Strangers", "It Could Be Sweet", "Wandering Star", "Numb", "Roads",
        "Pedestal", "Biscuit", "Glory Box"]),
    ("miles", "Kind of Blue", "1959-08-17", ["Jazz"], [
        "So What", "Freddie Freeloader", "Blue in Green", "All Blues", "Flamenco Sketches"]),
    ("amy", "Back to Black", "2006-10-27", ["R&B/Soul"], [
        "Rehab", "You Know I'm No Good", "Me & Mr Jones", "Just Friends", "Back to Black", "Love Is a Losing Game",
        "Tears Dry on Their Own", "Wake Up Alone", "Some Unholy War", "He Can Only Hold Her", "Addicted"]),
    ("floyd", "The Dark Side of the Moon", "1973-03-01", ["Rock"], [
        "Speak to Me", "Breathe", "On the Run", "Time", "The Great Gig in the Sky", "Money"]),
    ("nirvana", "Nevermind", "1991-09-24", ["Alternative", "Rock"], [
        "Smells Like Teen Spirit", "In Bloom", "Come as You Are", "Breed", "Lithium", "Polly"]),
    ("mac", "Rumours", "1977-02-04", ["Rock", "Pop"], [
        "Second Hand News", "Dreams", "Never Going Back Again", "Don't Stop", "Go Your Own Way", "Songbird"]),
    ("mj", "Thriller", "1982-11-30", ["Pop", "R&B/Soul"], [
        "Wanna Be Startin' Somethin'", "Baby Be Mine", "The Girl Is Mine", "Thriller", "Beat It", "Billie Jean"]),
    ("kendrick", "To Pimp a Butterfly", "2015-03-15", ["Hip-Hop/Rap"], [
        "Wesley's Theory", "For Free? (Interlude)", "King Kunta", "Institutionalized", "These Walls", "u",
        "Alright"]),
    ("norah", "Come Away with Me", "2002-02-26", ["Jazz"], [
        "Don't Know Why", "Seven Years", "Cold, Cold Heart", "Feelin' the Same Way", "Come Away with Me",
        "Shoot the Moon"]),
    ("eno", "Ambient 1: Music for Airports", "1978-03-01", ["Ambient"], ["1/1", "2/1", "1/2", "2/2"]),
    ("aphex", "Selected Ambient Works 85-92", "1992-02-12", ["Electronic", "Ambient"], [
        "Xtal", "Tha", "Pulsewidth", "Ageispolis", "i", "Green Calx"]),
    ("cash", "American IV: The Man Comes Around", "2002-11-05", ["Country"], [
        "The Man Comes Around", "Hurt", "Give My Love to Rose", "Bridge over Troubled Water", "I Hung My Head",
        "The First Time Ever I Saw Your Face"]),
    ("foxes", "Fleet Foxes", "2008-06-03", ["Folk"], [
        "Sun It Rises", "White Winter Hymnal", "Ragged Wood", "Tiger Mountain Peasant Song", "Quiet Houses",
        "He Doesn't Know Why"]),
    ("dua", "Future Nostalgia", "2020-03-27", ["Pop", "Dance"], [
        "Future Nostalgia", "Don't Start Now", "Cool", "Physical", "Levitating", "Break My Heart"]),
    ("metallica", "Master of Puppets", "1986-03-03", ["Metal"], [
        "Battery", "Master of Puppets", "The Thing That Should Not Be", "Welcome Home (Sanitarium)",
        "Disposable Heroes", "Leper Messiah"]),
    ("daftpunk", "Homework", "1997-01-20", ["Electronic", "Dance"], [
        "Daftendirekt", "WDPK 83.7 FM", "Revolution 909", "Da Funk", "Phoenix", "Fresh", "Around the World"]),
    ("massive", "Mezzanine", "1998-04-20", ["Electronic"], [
        "Angel", "Risingson", "Teardrop", "Inertia Creeps", "Exchange", "Dissolved Girl", "Man Next Door"]),
    ("verve", "Urban Hymns", "1997-09-29", ["Alternative", "Rock"], [
        "Bitter Sweet Symphony", "Sonnet", "The Rolling People", "The Drugs Don't Work", "Catching the Butterfly",
        "Neon Wilderness", "Space and Time", "Weeping Willow"]),
    ("pulp", "Different Class", "1995-10-30", ["Alternative", "Rock"], [
        "Mis-Shapes", "Pencil Skirt", "Common People", "I Spy", "Disco 2000", "Live Bed Show", "Something Changed"]),
    ("blur", "Parklife", "1994-04-25", ["Alternative", "Rock"], [
        "Girls & Boys", "Tracy Jacks", "End of a Century", "Parklife", "Bank Holiday", "Badhead",
        "The Debt Collector"]),
    ("beck", "Odelay", "1996-06-18", ["Alternative"], [
        "Devil's Haircut", "Hotwax", "Lord Only Knows", "The New Pollution", "Derelict", "Novacane", "Jack-Ass"]),
    ("moby", "Play", "1999-05-17", ["Electronic"], [
        "Honey", "Find My Baby", "Porcelain", "Natural Blues", "South Side", "Why Does My Heart Feel So Bad?",
        "Bodyrock"]),
]



def _build_demo_catalog() -> Catalog:
    artists = {f"d{key}": {"name": name, "genres": [*genres, "Music"]} for key, (name, genres) in _DEMO_ARTISTS.items()}
    albums: dict[str, tuple] = {}
    songs: list[SongRow] = []
    ids: dict[tuple[str, str], str] = {}  # (album title, track title) -> song id
    for n, (key, title, date, genres, tracks) in enumerate(_DEMO_ALBUMS, 1):
        alb_id = f"dalb{n}"
        albums[alb_id] = (title, f"d{key}", date)
        for position, track in enumerate(tracks, 1):
            sid = f"d{len(songs) + 1}"
            ids[(title, track)] = sid
            songs.append((sid, track, f"d{key}", genres, date, alb_id,
                          f"GBAYE{date[2:4]}{len(songs) + 1:05d}", position))

    album_ids = {title: [sid for sid, *_ in songs if albums[next(r[5] for r in songs if r[0] == sid)][0] == title]
                 for title in {a[0] for a in albums.values()}}

    def nth(album: str, position: int) -> str:
        return album_ids[album][position - 1]

    # The fictional listener: mostly 90s and 2000s British guitar bands and electronic acts
    known = ["radiohead", "muse", "oasis", "bjork", "daftpunk", "portishead", "nirvana", "blur", "pulp", "verve",
             "massive", "amy", "beck", "moby"]
    by_artist: dict[str, list[str]] = {}
    for key, title, *_ in _DEMO_ALBUMS:
        by_artist.setdefault(key, []).append(title)
    library = [nth(titles[0], pos) for key in known for titles in [by_artist[key]] for pos in (2, 5)]
    library += [nth(by_artist["radiohead"][n], 4) for n in (1, 2, 3)]
    recent = [nth(titles[0], pos) for key in known for titles in [by_artist[key]] for pos in (1, 4)]
    recent += [nth(by_artist["radiohead"][n], 1) for n in (1, 2, 3)] * 2  # on repeat
    recent += [nth(by_artist["muse"][1], 2), nth(by_artist["bjork"][1], 2)] * 2
    charts_by = [("Black Holes and Revelations", 2), ("Discovery", 1), ("Back to Black", 1),
                 ("(What's the Story) Morning Glory?", 3), ("Post", 1), ("Future Nostalgia", 5),
                 ("Future Nostalgia", 2), ("Kind of Blue", 1), ("The Bends", 3), ("Origin of Symmetry", 10),
                 ("Dummy", 2), ("Kid A", 3), ("Thriller", 6), ("Nevermind", 1), ("Rumours", 2),
                 ("To Pimp a Butterfly", 7), ("Thriller", 5), ("Rumours", 5), ("Master of Puppets", 1),
                 ("Come Away with Me", 1), ("The Dark Side of the Moon", 6), ("Fleet Foxes", 2),
                 ("American IV: The Man Comes Around", 2), ("Future Nostalgia", 4), ("Post", 2)]
    charts = [nth(album, pos) for album, pos in charts_by]
    charts += [sid for ids_ in album_ids.values() for sid in ids_[:2] if sid not in charts][:15]  # plus album openers
    # Similar artists: a few that share a genre, then wildcards from further afield, so discovery has somewhere to go
    order = list(artists)
    similar: dict[str, list[str]] = {}
    for aid, a in artists.items():
        near = [o for o in order if o != aid and set(a["genres"]) & set(artists[o]["genres"]) - {"Music"}][:5]
        far = [o for o in order[order.index(aid) + 1:] + order[:order.index(aid)] if o not in near][::2][:5]
        similar[aid] = near + far
    return Catalog(
        artists=artists, songs=songs, albums=albums,
        similar=similar,
        content_ratings={},
        playlist_id="pl.demo-alt-essentials", playlist_name="Alt Essentials",
        playlist_songs=[s[0] for s in songs[::5]][:40],
        library_songs=library, ratings={ids[("Kid A", "Everything In Its Right Place")]: 1,
                                        ids[("Homogenic", "Jóga")]: 1, ids[("In Rainbows", "Nude")]: 1,
                                        ids[("Origin of Symmetry", "Feeling Good")]: -1},
        recent_tracks=recent, library_artists=[f"d{k}" for k in known[:6]], charts=charts,
        recently_added_album="dalb7", top_songs=6, spread_top_songs=True,
    )


DEMO_CATALOG = _build_demo_catalog()


# ── Server ───────────────────────────────────────────────────────

class MockAppleMusic:
    """Start with .start(); read .url; inspect .requests; stop with .stop()."""

    def __init__(self, port: int = 0, catalog: Catalog | None = None):
        self.catalog = catalog or SMALL_CATALOG
        self.requests: list[dict] = []
        self.playlists: list[dict] = []
        self._port = port
        self._server: ThreadingHTTPServer | None = None

    @property
    def url(self) -> str:
        assert self._server is not None, "start() the mock first"
        return f"http://127.0.0.1:{self._server.server_address[1]}"

    def start(self) -> "MockAppleMusic":
        mock = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):  # keep test output quiet
                pass

            def _send(self, status: int, body: dict | None = None):
                payload = b"" if body is None else json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def _handle(self, method: str):
                url = urlparse(self.path)
                query = parse_qs(url.query)
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length).decode() if length else ""
                try:
                    body = json.loads(raw) if raw else None
                except json.JSONDecodeError:
                    body = raw
                auth = self.headers.get("Authorization", "").startswith("Bearer ")
                user = bool(self.headers.get("Music-User-Token"))
                mock.requests.append({"method": method, "path": unquote(url.path), "query": query,
                                      "body": body, "auth": auth, "user_token": user})
                status: int
                payload: dict | None
                if not auth:
                    status, payload = 401, {"errors": [{"status": "401"}]}
                elif "/me/" in url.path + "/" and not user:
                    status, payload = 403, {"errors": [{"status": "403"}]}
                else:
                    status, payload = mock.route(method, unquote(url.path), query, body)
                self._send(status, payload)

            def do_GET(self):
                self._handle("GET")

            def do_POST(self):
                self._handle("POST")

            def do_PUT(self):
                self._handle("PUT")

            def do_DELETE(self):
                self._handle("DELETE")

        self._server = LoopbackHTTPServer(("127.0.0.1", self._port), Handler)
        # A short poll interval keeps stop() fast: shutdown() waits for the next poll (default 0.5 s).
        threading.Thread(target=self._server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True).start()
        return self

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()

    def writes(self) -> list[dict]:
        return [r for r in self.requests if r["method"] != "GET"]

    # ── Routing ──────────────────────────────────────────────────

    def route(self, method: str, path: str, q: dict, body) -> tuple[int, dict | None]:
        cat = self.catalog
        parts = [p for p in path.split("/") if p]  # v1, ...
        if parts[:1] != ["v1"]:
            return 404, {"errors": [{"status": "404"}]}
        rest = parts[1:]

        if method == "GET":
            if rest == ["storefronts", "us"] or rest == ["me", "storefront"]:
                return 200, {"data": [{"id": "us", "type": "storefronts"}]}
            if rest == ["me", "recent", "played", "tracks"]:
                offset = int(q.get("offset", ["0"])[0])
                return 200, {"data": [cat.song(s) for s in cat.recent_tracks] if offset == 0 else []}
            if rest == ["me", "history", "heavy-rotation"] or rest == ["me", "recommendations"]:
                return 200, {"data": []}
            if rest == ["me", "recent", "played"]:
                return 200, {"data": []}
            if rest == ["me", "ratings", "songs"]:
                return 200, {"data": [{"id": sid, "type": "ratings", "attributes": {"value": v}}
                                      for sid, v in cat.ratings.items()]}
            if rest == ["me", "music-summaries"] or rest == ["me", "music-summaries", "milestones"]:
                return 404, {"errors": [{"status": "404", "title": "Replay not available"}]}
            if rest == ["me", "library", "artists"]:
                offset = int(q.get("offset", ["0"])[0])
                return 200, {"data": [{"id": f"r.{a}", "type": "library-artists",
                                       "attributes": {"name": cat.artists[a]["name"]}}
                                      for a in cat.library_artists] if offset == 0 else []}
            if rest == ["me", "library", "songs"]:
                offset = int(q.get("offset", ["0"])[0])
                out = []
                for sid in cat.library_songs if offset == 0 else []:
                    s = cat.song(sid)
                    s["id"] = f"i.{sid}"
                    s["type"] = "library-songs"
                    s["relationships"]["catalog"] = {"data": [{"id": sid, "type": "songs"}]}
                    out.append(s)
                return 200, {"data": out}
            if rest == ["me", "library", "recently-added"]:
                return 200, {"data": [
                    {"id": f"l.{cat.recently_added_album}", "type": "library-albums",
                     "attributes": {"name": cat.albums[cat.recently_added_album][0],
                                    "artistName": cat.artists[cat.albums[cat.recently_added_album][1]]["name"],
                                    "genreNames": ["Alternative"],
                                    "releaseDate": cat.albums[cat.recently_added_album][2]}},
                    {"id": "p.1", "type": "library-playlists", "attributes": {"name": "Road Trip"}},
                ]}
            if rest == ["me", "recent", "radio-stations"]:
                return 200, {"data": [
                    {"id": "ra.1", "type": "stations", "attributes": {"name": "Alternative Radio"}},
                    {"id": "ra.2", "type": "stations", "attributes": {"name": "Radiohead Station"}},
                ]}
            if rest == ["me", "library", "playlists"]:
                return 200, {"data": self.playlists}
            if rest[:3] == ["me", "library", "playlists"] and rest[-1] == "tracks":
                return 200, {"data": []}
            if rest[:1] == ["catalog"]:
                return self._catalog(rest[2:], q)
            return 404, {"errors": [{"status": "404", "detail": f"no mock for GET {path}"}]}

        if method == "POST":
            if rest == ["me", "library", "playlists"]:
                attrs = (body or {}).get("attributes", {})
                pl = {"id": f"p.{len(self.playlists) + 1}", "type": "library-playlists",
                      "attributes": {"name": attrs.get("name", "")}}
                self.playlists.append(pl)
                return 201, {"data": [pl]}
            if rest == ["me", "library"] or rest == ["me", "favorites"]:
                return 202, None
            if rest[:3] == ["me", "library", "playlists"] and rest[-1] == "tracks":
                return 204, None
        if method == "PUT" and rest[:3] == ["me", "ratings", "songs"] and len(rest) == 4:
            value = ((body or {}).get("attributes") or {}).get("value")
            return 200, {"data": [{"id": rest[3], "type": "ratings", "attributes": {"value": value}}]}
        if method == "DELETE" and rest[:3] == ["me", "ratings", "songs"] and len(rest) == 4:
            return 204, None
        if method == "DELETE" and rest[:3] == ["me", "library", "playlists"] and rest[-1] == "tracks":
            return 204, None
        return 404, {"errors": [{"status": "404", "detail": f"no mock for {method} {path}"}]}

    @staticmethod
    def _playlist_page(cat: "Catalog", offset: int) -> dict:
        ids = cat.playlist_songs[offset:offset + cat.playlist_page_size]
        page: dict = {"data": [cat.song(sid) for sid in ids]}
        if offset + len(ids) < len(cat.playlist_songs):
            page["next"] = f"/v1/catalog/us/playlists/{cat.playlist_id}/tracks?offset={offset + len(ids)}"
        return page

    def _catalog(self, rest: list[str], q: dict) -> tuple[int, dict]:
        cat = self.catalog
        if rest == ["charts"]:
            return 200, {"results": {"songs": [{"name": "Top Songs", "data": [cat.song(sid) for sid in cat.charts]}]}}
        if rest == ["genres"]:
            return 200, {"data": [{"id": "20", "type": "genres", "attributes": {"name": "Alternative"}}]}
        if rest == ["search"]:
            term = (q.get("term", [""])[0]).lower()
            types = (q.get("types", ["songs"])[0]).split(",")
            results: dict = {}
            if "artists" in types:
                results["artists"] = {"data": [cat.artist(a) for a, v in cat.artists.items() if v["name"].lower() in term
                                               or term in v["name"].lower()]}
            if "songs" in types:
                results["songs"] = {"data": [cat.song(r[0]) for r in cat.songs
                                             if r[1].lower() in term or term in r[1].lower()
                                             or cat.artists[r[2]]["name"].lower() in term]}
            if "albums" in types:
                results["albums"] = {"data": [cat.album(a) for a, v in cat.albums.items() if term in v[0].lower()]}
            return 200, {"results": results}
        if rest == ["songs"]:
            wanted = set((q.get("filter[isrc]", [""])[0]).split(","))
            return 200, {"data": [cat.song(r[0]) for r in cat.songs if r[6] in wanted]}
        if len(rest) == 2 and rest[0] == "songs":
            if not any(r[0] == rest[1] for r in cat.songs):
                return 404, {"errors": [{"status": "404", "detail": f"no song {rest[1]}"}]}
            return 200, {"data": [cat.song(rest[1])]}
        if rest[:1] == ["artists"] and len(rest) >= 2 and rest[1] in cat.artists:
            aid = rest[1]
            if rest[2:] == ["view", "similar-artists"]:
                return 200, {"data": [cat.artist(a) for a in cat.similar.get(aid, [])]}
            if rest[2:] == ["albums"]:
                return 200, {"data": [cat.album(a) for a, v in cat.albums.items() if v[1] == aid]}
            if len(rest) == 2 and "top-songs" in (q.get("views", [""])[0]):
                tops = cat.top_songs_for(aid)
                a = cat.artist(aid)
                a["views"] = {"top-songs": {"data": tops}}
                return 200, {"data": [a]}
            if len(rest) == 2:
                return 200, {"data": [cat.artist(aid)]}
        if len(rest) == 2 and rest[0] == "playlists" and rest[1] == cat.playlist_id:
            page = self._playlist_page(cat, 0)
            return 200, {"data": [{
                "id": cat.playlist_id, "type": "playlists",
                "attributes": {"name": cat.playlist_name, "curatorName": "Apple Music Alternative"},
                "relationships": {"tracks": page}}]}
        if len(rest) == 3 and rest[0] == "playlists" and rest[1] == cat.playlist_id and rest[2] == "tracks":
            return 200, self._playlist_page(cat, int(q.get("offset", ["0"])[0]))
        if len(rest) == 2 and rest[0] == "albums" and rest[1] in cat.albums:
            a = cat.album(rest[1])
            a["relationships"] = {"tracks": {"data": [cat.song(r[0]) for r in cat.songs if r[5] == rest[1]]}}
            return 200, {"data": [a]}
        return 404, {"errors": [{"status": "404", "detail": f"no mock for catalog/{'/'.join(rest)}"}]}


# ── Demo mode ────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
DEMO_HOME = Path.home() / ".apple-music-dj-demo"
REAL_APP_DIR = Path.home() / ".apple-music-dj"
PROFILE_TOKEN = "DEMO_PROFILE"
BANNER = ("🎧 Demo mode: a fictional listener and a sample catalog. "
          "Nothing here touches your Apple Music account.")
# Scripts that act outside the sandbox (the system crontab, real credentials) or are not tools
NOT_IN_DEMO = {"demo.py", "setup_cron.py", "setup_auth.py", "generate_dev_token.py", "_common.py"}


def demo_profile_path() -> Path:
    return DEMO_HOME / ".apple-music-dj" / "taste_profile.json"


def demo_env(api_url: str) -> dict:
    """The child's environment: real Apple credentials removed, demo ones and a sandbox HOME set."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("APPLE_")}
    env.update({
        "HOME": str(DEMO_HOME),
        "APPLE_MUSIC_API_BASE": api_url,
        "APPLE_MUSIC_DEV_TOKEN": "demo-dev-token",
        "APPLE_MUSIC_USER_TOKEN": "demo-user-token",
        "APPLE_MUSIC_STOREFRONT": "us",
        "APPLE_MUSIC_DJ_DEMO": "1",
    })
    return env


def script_command(name: str) -> list[str]:
    """Resolve a skill script by bare name; anything else is refused."""
    if "/" in name or name in NOT_IN_DEMO or not (SCRIPT_DIR / name).is_file() or not name.endswith((".py", ".sh")):
        allowed = sorted(p.name for p in SCRIPT_DIR.iterdir()
                         if p.suffix in (".py", ".sh") and p.name not in NOT_IN_DEMO)
        raise SystemExit(f"ERROR: '{name}' can't run in demo mode. Pick one of: {', '.join(allowed)}")
    path = str(SCRIPT_DIR / name)
    return ["bash", path] if name.endswith(".sh") else [sys.executable, path]


def _points_into_real_data(value: str) -> bool:
    """True if `value`, read as a path (with `..` and symlinks resolved), is in the real data folder."""
    if not value:
        return False
    try:
        resolved = Path(value).expanduser().resolve()
        real = REAL_APP_DIR.resolve()
    except (OSError, RuntimeError, ValueError):
        return False
    return resolved == real or real in resolved.parents


def check_args(args: list[str]) -> list[str]:
    """Swap DEMO_PROFILE for the demo profile and refuse paths into the real data folder."""
    real_text = re.compile(re.escape(str(REAL_APP_DIR)) + r"(?=/|$)")
    out = []
    for a in args:
        value = a.split("=", 1)[1] if a.startswith("--") and "=" in a else a
        if real_text.search(a) or _points_into_real_data(value):
            raise SystemExit(f"ERROR: demo mode won't read or write your real data ({REAL_APP_DIR}). "
                             f"Use {PROFILE_TOKEN} for the demo profile.")
        out.append(a.replace(PROFILE_TOKEN, str(demo_profile_path())))
    return out


def _run(cmd: list[str], env: dict, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, env=env, text=True, capture_output=capture, timeout=300)


# Bump when DEMO_CATALOG changes: a demo profile built against an older catalog names artists the new one lacks.
DEMO_CATALOG_VERSION = "2"


def ensure_profile(env: dict) -> None:
    marker = demo_profile_path().with_name("demo_catalog_version")
    if demo_profile_path().is_file():
        if marker.is_file() and marker.read_text().strip() == DEMO_CATALOG_VERSION:
            return
        demo_profile_path().unlink()  # built from an older catalog; rebuild it
    r = _run(script_command("taste_profiler.py") + ["--output", str(demo_profile_path()), "--skip-replay"],
             env, capture=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit("ERROR: could not build the demo taste profile.")
    marker.write_text(DEMO_CATALOG_VERSION + "\n")


def prepare_demo_home() -> None:
    """Create the sandbox, refusing a symlinked one (it could alias the real data folder)."""
    inner = DEMO_HOME / ".apple-music-dj"
    for d in (DEMO_HOME, inner):
        if d.is_symlink():
            raise SystemExit(f"ERROR: {d} is a symlink; demo mode needs a real folder there. "
                             f"Remove the link and try again.")
    DEMO_HOME.mkdir(mode=0o700, exist_ok=True)
    if DEMO_HOME.resolve() == REAL_APP_DIR.resolve() or REAL_APP_DIR.resolve() in DEMO_HOME.resolve().parents:
        raise SystemExit(f"ERROR: {DEMO_HOME} resolves into {REAL_APP_DIR}; refusing to run the demo there.")


def start_server() -> MockAppleMusic:
    prepare_demo_home()
    return MockAppleMusic(catalog=DEMO_CATALOG).start()


def cmd_run(script: str, args: list[str]) -> int:
    cmd = script_command(script) + check_args(args)
    print(BANNER, file=sys.stderr)
    srv = start_server()
    try:
        env = demo_env(srv.url)
        if any(PROFILE_TOKEN in a for a in args):
            ensure_profile(env)
        return _run(cmd, env).returncode
    finally:
        srv.stop()


TOUR = [
    ("Your Taste DNA card", ["taste_card.py", PROFILE_TOKEN, "--format", "text"]),
    ('"Songs like Radiohead" (a preview; in real use you approve before anything is created)',
     ["strategy_engine.py", "--strategy", "similar", "--similar-to", "Radiohead", "--profile", PROFILE_TOKEN,
      "--size", "8"]),
    ('"Make me a 90s throwback"',
     ["strategy_engine.py", "--strategy", "era", "--decade", "1990s", "--profile", PROFILE_TOKEN, "--size", "8"]),
    ('"Give me one song for today"', ["daily_pick.py", "daily", PROFILE_TOKEN, "us"]),
    ('"How compatible am I with Björk?"', ["compatibility.py", "artist", PROFILE_TOKEN, "us", "Björk"]),
]


def pretty(stdout: str) -> str:
    """Playlists read as a numbered list with reasons; anything else is passed through."""
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return stdout.rstrip()
    if isinstance(data, dict) and isinstance(data.get("tracks"), list):
        rows = [f"{data.get('name', 'Playlist')}"]
        width = max((len(f"{t.get('name')} — {t.get('artist')}") for t in data["tracks"]), default=0)
        for i, t in enumerate(data["tracks"], 1):
            label = f"{t.get('name')} — {t.get('artist')}"
            rows.append(f"{i:>2}. {label.ljust(width)}   {t.get('reason', '')}".rstrip())
        return "\n".join(rows)
    if isinstance(data, dict) and isinstance(data.get("message"), str):
        return data["message"]
    if isinstance(data, dict) and "compatibility_pct" in data:
        return f"{data.get('artist')}: {data['compatibility_pct']}% — {data.get('verdict', '')}".rstrip(" —")
    return json.dumps(data, indent=2, ensure_ascii=False)


def cmd_tour() -> int:
    print(BANNER + "\n")
    srv = start_server()
    try:
        env = demo_env(srv.url)
        print("── Building a taste profile from the demo listener's history ──\n")
        ensure_profile(env)
        failed = []
        for title, (script, *args) in TOUR:
            print(f"\n── {title} ──\n", flush=True)
            r = _run(script_command(script) + check_args(args), env, capture=True)
            if r.returncode == 0:
                print(pretty(r.stdout))
            else:
                failed.append(script)
                print(r.stderr.rstrip() or f"({script} exited {r.returncode})")
    finally:
        srv.stop()
    if failed:
        print(f"\n⚠️  {len(failed)} demo step(s) failed: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("\n── That's the demo ──")
    print("Ready for your own music? Run: python3 scripts/setup_auth.py  (see references/auth-setup.md)")
    return 0


def cmd_serve(port: int) -> int:
    srv = MockAppleMusic(port, DEMO_CATALOG).start()
    print(f"Mock Apple Music API on {srv.url}  (Ctrl-C to stop)", flush=True)
    try:
        with contextlib.suppress(KeyboardInterrupt):  # Ctrl-C is the normal way to stop
            threading.Event().wait()
    finally:
        srv.stop()
    return 0


def cmd_reset() -> int:
    if DEMO_HOME.is_dir() and not DEMO_HOME.is_symlink():
        shutil.rmtree(DEMO_HOME)
        print(f"Removed {DEMO_HOME}")
    else:
        print("No demo data to remove.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Try Apple Music DJ with a fictional listener — no tokens needed.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tour", help="Guided tour: taste profile, card, playlists, compatibility")
    run = sub.add_parser("run", help="Run one skill script in demo mode (DEMO_PROFILE = demo profile path)")
    run.add_argument("script", help="Script name in scripts/, e.g. strategy_engine.py")
    run.add_argument("args", nargs=argparse.REMAINDER, help="Arguments passed to the script")
    serve = sub.add_parser("serve", help="Serve the mock API on 127.0.0.1 (development)")
    serve.add_argument("--port", type=int, default=8765)
    sub.add_parser("reset", help=f"Delete the demo data folder ({DEMO_HOME})")
    a = parser.parse_args(argv)
    if a.cmd == "tour":
        return cmd_tour()
    if a.cmd == "run":
        return cmd_run(a.script, a.args)
    if a.cmd == "serve":
        return cmd_serve(a.port)
    return cmd_reset()


if __name__ == "__main__":
    sys.exit(main())
