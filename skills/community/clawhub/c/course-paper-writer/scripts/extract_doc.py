"""Minimal Word 97 (.doc) text extractor: OLE2 compound file -> FIB -> piece table."""
import struct
import sys


def read_ole(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "not an OLE2 file"
    ssz = 1 << struct.unpack_from("<H", data, 0x1E)[0]
    mssz = 1 << struct.unpack_from("<H", data, 0x20)[0]
    n_fat = struct.unpack_from("<I", data, 0x2C)[0]
    dir_start = struct.unpack_from("<I", data, 0x30)[0]
    mini_cutoff = struct.unpack_from("<I", data, 0x38)[0]
    minifat_start = struct.unpack_from("<I", data, 0x3C)[0]
    difat_start = struct.unpack_from("<I", data, 0x44)[0]
    n_difat = struct.unpack_from("<I", data, 0x48)[0]

    def sector(i):
        off = (i + 1) * ssz
        return data[off:off + ssz]

    # DIFAT
    difat = list(struct.unpack_from("<109I", data, 0x4C))
    nxt = difat_start
    per = ssz // 4 - 1
    while nxt not in (0xFFFFFFFF, 0xFFFFFFFE) and n_difat > 0:
        blk = sector(nxt)
        vals = struct.unpack_from("<%dI" % (per + 1), blk, 0)
        difat.extend(vals[:per])
        nxt = vals[per]
    fat_sectors = [x for x in difat if x < 0xFFFFFFF0][:n_fat]

    fat = []
    for s in fat_sectors:
        fat.extend(struct.unpack_from("<%dI" % (ssz // 4), sector(s), 0))

    def chain(start):
        out, cur, seen = [], start, set()
        while cur < 0xFFFFFFF0 and cur not in seen:
            seen.add(cur)
            out.append(cur)
            cur = fat[cur] if cur < len(fat) else 0xFFFFFFFE
        return out

    def read_chain(start, size=None):
        buf = b"".join(sector(s) for s in chain(start))
        return buf[:size] if size is not None else buf

    root = None
    dirs = []
    for s in chain(dir_start):
        blk = sector(s)
        for off in range(0, ssz, 128):
            e = blk[off:off + 128]
            if len(e) < 128:
                continue
            nlen = struct.unpack_from("<H", e, 0x40)[0]
            name = e[:max(0, nlen - 2)].decode("utf-16-le", "ignore")
            typ = e[0x42]
            start = struct.unpack_from("<I", e, 0x74)[0]
            size = struct.unpack_from("<I", e, 0x78)[0]
            dirs.append((name, typ, start, size))
            if typ == 5:
                root = (start, size)

    ministream = b""
    if root:
        ministream = read_chain(root[0], root[1])
    minifat = []
    if minifat_start < 0xFFFFFFF0:
        raw = b"".join(sector(s) for s in chain(minifat_start))
        minifat = list(struct.unpack_from("<%dI" % (len(raw) // 4), raw, 0))

    streams = {}

    def read_mini(start, size):
        out, cur, seen = [], start, set()
        while cur < 0xFFFFFFF0 and cur not in seen:
            seen.add(cur)
            out.append(ministream[cur * mssz:(cur + 1) * mssz])
            cur = minifat[cur] if cur < len(minifat) else 0xFFFFFFFE
        return b"".join(out)[:size]

    for name, typ, start, size in dirs:
        if typ != 2:
            continue
        if size < mini_cutoff:
            streams[name] = read_mini(start, size)
        else:
            streams[name] = read_chain(start, size)
    return streams


def extract_text(path):
    st = read_ole(path)
    wd = st.get("WordDocument")
    if wd is None:
        raise SystemExit("no WordDocument stream: %s" % list(st))
    flags = struct.unpack_from("<H", wd, 0x0A)[0]
    tbl = "1Table" if (flags & 0x0200) else "0Table"
    table = st.get(tbl) or st.get("1Table") or st.get("0Table")
    fc_clx, lcb_clx = struct.unpack_from("<II", wd, 0x01A2)
    clx = table[fc_clx:fc_clx + lcb_clx]

    pos, plcf = 0, None
    while pos < len(clx):
        t = clx[pos]
        if t == 1:
            cb = struct.unpack_from("<H", clx, pos + 1)[0]
            pos += 3 + cb
        elif t == 2:
            lcb = struct.unpack_from("<I", clx, pos + 1)[0]
            plcf = clx[pos + 5:pos + 5 + lcb]
            break
        else:
            break
    if plcf is None:
        raise SystemExit("no piece table")

    n = (len(plcf) - 4) // 12
    cps = list(struct.unpack_from("<%dI" % (n + 1), plcf, 0))
    pieces = []
    off = 4 * (n + 1)
    for i in range(n):
        fc = struct.unpack_from("<I", plcf, off + 8 * i + 2)[0]
        compressed = bool(fc & 0x40000000)
        fcv = (fc & 0x3FFFFFFF) // 2 if compressed else fc
        pieces.append((cps[i], cps[i + 1], fcv, compressed))

    out = []
    for cp0, cp1, fc, compressed in pieces:
        ln = cp1 - cp0
        if compressed:
            raw = wd[fc:fc + ln]
            out.append(raw.decode("cp1252", "replace"))
        else:
            raw = wd[fc:fc + ln * 2]
            out.append(raw.decode("utf-16-le", "replace"))
    text = "".join(out)
    text = text.replace("\r", "\n").replace("\x07", "\n").replace("\x0b", "\n")
    text = text.replace("\x0c", "\n").replace("\x01", "").replace("\x02", "")
    text = text.replace("\x08", "").replace("\x13", "").replace("\x14", "").replace("\x15", "")
    return text


if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else None
    txt = extract_text(src)
    if dst:
        open(dst, "w", encoding="utf-8").write(txt)
        print("wrote", dst, len(txt), "chars")
    else:
        print(txt)
