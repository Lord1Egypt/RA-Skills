# Anytype — My Setup

This file holds instance-specific config for the Anytype skill. Not for publishing.

## Space

- **Primary space ID:** `bafyreial7tzkey5sntoizw7scv2lrywqdicd7m6ru2k6wae7w3z6igm5ke.1f4pitw5ca9gc`
- **Invite ID:** `bafybeifel75s42deh74lbjx3socdyung4ojspjgbr64jxrduf3dghlx35i`
- **Hash:** `CvFB12csDDVDpYxi5J1FewXmdsLmifnLx4p3fBCRG6Jt`
- **Public link format:** `https://object.any.coop/{object_id}?spaceId={space_id}&inviteId={invite_id}#{hash}`

## Known Collections

| Name | Object ID |
|------|-----------|
| Merkys — Healthcare Chatbot | `bafyreicm3a7xj6zhq2l3ouuo74klcxixnvilo3xif24yoijb4wghjpepm4` |
| Mercoder.ai | `bafyreigvkwfrtbmrkureuoxfj4ewjrccvpla7dndd7d3ygsyjxuqzorgja` |
| Vibe Coding Metrics | `bafyreicejuvonwzo5sgjieana65l4pjbsrhlij5fpbjdrbjc5kdogwwalu` |

## Tag Property

- **Property key:** `tag`
- **Property ID:** `bafyreicsoqz7qja7uqrpfvtub4c4gg7djsv24ojc42em6j3a2ctaeiy7r4`

## Defined Tags

| Tag name | Tag ID | Use for |
|----------|--------|---------|
| `merkys` | `bafyreiatxjki2c6zy6pyxf6e3xkfnjheqvfmajhqmtpyssiw6wvz3z4x3e` | Merkys chatbot pages |
| `mercoder` | `bafyreibmnkru5tu4ltfo6xwu5ijmzgt54dy5dsbekz7l7ppxqjrntgceam` | Mercoder.ai pages |
| `vibe-coding` | `bafyreib5fo4pfeq5s46akb6wqk4jufu3j63cp5ay5wrxn2hda2bbtdo3ou` | Vibe coding metrics |
| `paceflow` | `bafyreicnhcmlzav2olnejjpgi6mznthckbheypbwddxtrrsekddmqojica` | Paceflow product pages |
| `call-notes` | `bafyreicuka2zitbrqbae6khc7sse2mnwlcx3a3i2gig2jqvffknjyzt3fe` | Meeting/call notes |
| `research` | `bafyreihtobisskd2ctgs7r74k5gfa6tzejxdtf5qkbyvac6okdgj43uv4y` | Research documents |
| `product` | `bafyreib27tsqjemixmc76yam7ui66x4dsp2vncwbqd7ci7c7mwkqp7gvba` | Product strategy/roadmap |
| `hub` | `bafyreic2y3u3iai4z36wrnebj4pejstdkov7p3oj6dokho5xhmaog27jzi` | Hub/index pages |
| `healthcare` | `bafyreid3nw4casmj4obscsk53jwowbs7x2yjgsm6l4guivrr4nmts5r42i` | Healthcare domain |
| `devops` | `bafyreieqpordkymw7jo5lp3habdyqomytp7bvtpxvwt4m32zby3kcbs3au` | DevOps/infrastructure |
| `security` | `bafyreieazhkkfmtojxin6d35fh5kgfdkqb6t25d77p2i6dkixsj5ppaqii` | Security topics |
| `ai` | `bafyreibdo3qelsyuapt44fbjjkhl3w6jnw3ohpqdzecs5rro4awjlawrwq` | AI/ML topics |

## Tagging Rules (project-specific)

- Always add the project tag (`merkys`, `mercoder`, `vibe-coding`, `paceflow`)
- Always add content type tag (`call-notes`, `research`, `product`, `hub`)
- Add domain tag when relevant (`healthcare`, `devops`, `security`, `ai`)
- Hub pages always get `hub` tag

## Custom Properties

- **`related_pages`** (key: `related_pages`, format: `objects`) — writable via API; use for linking objects in the graph
