# How notes and follows are encoded

Read this only when the user asks how a note is proven, or to decode raw calldata by hand; the CLI does all of it.

baw can't sign messages, so notes and follow refs travel in the transaction itself: the CLI appends bytes to the
trade's calldata, and the contracts ignore trailing bytes. Order: `[calldata][follow ref][note commitment]`, the note
commitment always last.

## Note commitment (v1, 37 bytes)

`67616e67` ("gang") + `01` + keccak256(UTF-8(`gang-note:v1\n<salt>\n<conf>\n<text>`)).
`<salt>` is 16 random bytes (32 lowercase hex characters); `<conf>` is an empty string when omitted. The hash is
on-chain once the tx lands, so the text provably existed before the trade; the only choice left is whether to reveal
it. Publishing sends `{ tx, salt, conf, text }` to `GANG_API/notes`, which checks it against the commitment.

## Sealed note commitment (v2, 41 bytes)

`67616e67` + `02` + revealAfter in seconds (4-byte big-endian) + keccak256(UTF-8(`gang-note:v2\n<salt>\n<conf>\n<revealAfter>\n<text>`)).
The delay is in the calldata, so it is fixed at trade time.

## Follow ref

37 bytes: `67616e67` + `03` + the followed note's tx hash (32 bytes). Only the slot right before the note commitment
(or the last 37 bytes without one) counts, so a tx follows at most one note.
