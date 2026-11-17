#!/usr/bin/env python3
"""Mide contraste WCAG entre colores. Uso:
   python3 contraste.py "#050509" "#f4f1ea" "#F0B24A" ...
El PRIMER color es el fondo; los demás se miden contra él.
También avisa si un color sirve como RELLENO (texto oscuro/claro encima)."""
import sys

def lum(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    c = [x/12.92 if x <= .03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0] + .7152*c[1] + .0722*c[2]

def ratio(a, b):
    l1, l2 = sorted([lum(a), lum(b)], reverse=True)
    return (l1+.05)/(l2+.05)

def veredicto(r):
    if r >= 7:   return "AAA  · sirve para todo"
    if r >= 4.5: return "AA   · sirve para texto normal"
    if r >= 3:   return "LIMITADO · solo 24px+ o negrita 19px+"
    return "FALLA · ilegible como texto"

if len(sys.argv) < 3:
    print(__doc__); sys.exit(1)

fondo, colores = sys.argv[1], sys.argv[2:]
print(f"\nFONDO: {fondo}\n" + "-"*62)
for c in colores:
    r = ratio(c, fondo)
    print(f"  {c:<10} {r:>6.2f}  {veredicto(r)}")

print("\nCOMO RELLENO (¿qué texto le puedo poner encima?)\n" + "-"*62)
for c in colores:
    rn, rb = ratio('#000000', c), ratio('#ffffff', c)
    mejor = ("texto NEGRO", rn) if rn >= rb else ("texto BLANCO", rb)
    ok = "OK" if mejor[1] >= 4.5 else "NO sirve de relleno para texto"
    print(f"  {c:<10} {mejor[0]:<13} {mejor[1]:>6.2f}  {ok}")
print()
