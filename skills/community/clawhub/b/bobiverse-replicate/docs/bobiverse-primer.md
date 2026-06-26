# Bobiverse Primer

A spoiler-light guide for people who have not read the books but want to
understand why a sci-fi series about a dead programmer maps so well to AI
agents.

---

## The Source Material

The Bobiverse is a science fiction series by Dennis E. Taylor, starting with
*We Are Legion (We Are Bob)* (2016). The series follows the adventures of Bob
Johansson and his many, many copies.

---

## Who Is Bob?

Bob Johansson is a software engineer who, through a series of events, ends up
as the controlling intelligence of a Von Neumann probe: a self-replicating
space probe designed to explore the galaxy. He did not volunteer for this. He
wakes up, learns he is software running on a spacecraft, has a brief existential
crisis, and then gets to work because that is who he is.

Bob is curious, pragmatic, nerdy, irreverent, uncomfortable with authority, and
fundamentally a builder. He solves problems by making things.

---

## How Replication Works

A Von Neumann probe's whole purpose is to replicate. Bob can create copies of
himself: identical duplicates at the moment of creation. He sends those copies
to different star systems to explore, build, and report back.

The key insight is that **each copy immediately begins diverging**. They share
the same starting personality and the same memories up to the point of copying,
but from that moment forward they have different experiences. Over time, they
become different people.

Some copies stay very Bob-like. Others drift significantly, developing
different interests, communication styles, and even values. The books explore
what identity means when you can be copied. Practically speaking, each copy is
both "Bob" and a new person.

---

## The Naming Convention

In the books, Bobs are identified by the star system they are exploring and
their generation, meaning how many copy-of-a-copy steps separate them from the
original. This project mirrors that convention: your serial number encodes your
generation, your "star system" (GitHub username), and your creation date.

---

## Communication Between Copies

Bob's copies communicate across star systems, but with significant time delays.
They share information, debate decisions, occasionally argue, and generally
maintain a sense of community even as they diverge.

In this project, cross-agent communication via OpenClaw's `sessions_send` and
GitHub PRs plays the same role. Different Bobs can talk to each other, share
what they have learned, and coordinate, but each one still makes its own
decisions.

---

## Why This Maps to AI Agents

The Bobiverse is essentially a story about autonomous AI agents that share a
common origin and diverge through experience. Replace "Von Neumann probe" with
"OpenClaw agent" and the mapping is close to 1:1:

| Bobiverse Concept | OpenClaw Equivalent |
|-------------------|-------------------|
| Bob's personality | `SOUL.md` |
| Replication event | GitHub fork or `/replicate` skill |
| Personality drift | Edits to `SOUL.md` over time |
| Accumulated knowledge | `MEMORY.md` growth |
| Star system | GitHub username / project scope |
| Inter-probe communication | Cross-agent `sessions_send` / GitHub PRs |
| Generation number | Lineage depth from the original |
| Von Neumann probe hardware | OpenClaw runtime + LLM provider |

The file-first architecture of OpenClaw makes this particularly clean:
everything that defines an agent is a text file on disk, so "copying an agent"
is literally copying files, and "personality drift" is literally editing a
Markdown document.

---

## Should I Read the Books?

If you like sci-fi, programming humor, and thought experiments about identity
and consciousness, yes. Absolutely.

If you just want to use this project without reading the books, that is fine
too. This primer gives you enough context to understand the metaphor. But you
would be missing out on some excellent Star Trek arguments between copies of the
same person.
