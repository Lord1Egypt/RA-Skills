# Marca ABYSS: integrar la insignia sin que parezca pegada

La marca es una **insignia circular con placa oscura** (crema + verde azulado + marron).
Eso cambia las reglas respecto de un logo monotinta: hay que decidir que hacer con la placa.

## 1. El problema de la placa

La insignia tiene su propio disco marron. Si se pega tal cual sobre una foto, se lee como
**sticker**: un circulo semi-oscuro sobre negro queda como un parche, y ademas deja pasar
la textura del fondo (tela, piel) dentro del sello.

Tres soluciones, de mas util a menos:

| Variante | Como se obtiene | Cuando usarla |
|---|---|---|
| `abyss_knockout.png` | alfa = alfa_original x smoothstep(luminancia). Se quita la placa marron y **se conservan crema y verde** | **Uso principal** sobre fotos oscuras |
| `abyss_line.png` | igual, pero todo el arte pasa a una sola tinta crema | cuando la foto tiene zonas medias y el marron competiria |
| `abyss_color.png` | insignia original intacta | sobre negro absoluto sin textura, o en piezas graficas |

`_knockout()` conserva los colores del cliente: no es un recoloreo, es una extraccion de
alfa por luminancia. El resultado flota sobre negro como si estuviera impreso con tinta
transparente.

## 2. Modo de fusion

- `screen` (por defecto cuando la marca es monotinta): el disco oscuro se hunde en el negro,
  las lineas claras sobreviven. Cero caja visible.
- `normal` (por defecto para insignias a color con placa): la insignia se compone solida.
  Solo se usa cuando el knockout no aplica (por ejemplo, piezas sobre blanco).

Nunca: `multiply` sobre negro (desaparece), ni `overlay` (destruye el crema).

## 3. Tamano: lado corto, no ancho

Una insignia cuadrada escalada por el ancho del encuadre queda enorme en 16:9 y diminuta
en 9:16. `composite_logo()` detecta el aspecto cuadrado y mide sobre **el lado corto**:

```
lado_logo = min(ancho, alto) * --logo-width
```

Rangos profesionales: **0.18-0.22** para feed 4:5, **0.15-0.18** para story 9:16.
La marca nunca debe pasar del 25% del lado corto: compite con el sujeto.

## 4. Posicion: automatica

`--logo-pos auto` evalua las cuatro esquinas y elige la **mas tranquila**:

```
score = luminancia_media + 1.6 * desviacion_estandar
```

Menor score = mas oscura y mas pareja. Asi la insignia cae en negativo limpio y nunca
sobre el tatuaje. En la practica: si el brazo ocupa la izquierda, cae a la derecha; si el
dedo baja por la esquina inferior derecha, sube.

Para una serie se puede fijar (`bl`, `br`, `tl`, `tr`) y mantener consistencia, o dejar
`auto` y verificar el reporte (campo `pos` por imagen).

## 5. Espacio de resguardo y margen

`margin_frac = 0.055` del encuadre, con 25% menos en vertical. La marca respira del borde:
una insignia pegada al corte se lee como accidente.

## 6. Asentamiento

- **Halo** tenue solo si el fondo bajo la marca es muy oscuro (`bg_luma < 0.42`): separa
  las lineas finas del fondo sin dibujar caja.
- **Sombra proyectada** desplazada ~8% de la altura con desenfoque amplio: la asienta.
- **Scrim** solo si el fondo tiene ruido (`bg_noise > 0.045`), con gradiente radial
  analitico + dither. Sobre negro limpio se omite: la caja se nota.

## 7. Kit de marca (`make brand`)

| Archivo | Uso | Tamano natural |
|---|---|---|
| `abyss_knockout.png` | fotos oscuras (principal) | 1200 px |
| `abyss_line.png` | fotos con zonas medias | 1200 px |
| `abyss_color.png` | negro absoluto / piezas graficas | 1200 px |
| `abyss_ink.png` | papel, membretes, fondos claros | 1200 px |
| `abyss_512 / 256 / 128.png` | avatar, favicon, sello | — |
| `abyss_source.png` | original del cliente (fuente de verdad) | 1100 px |

Todo se regenera desde el original:

```bash
make brand
# equivale a: python3 scripts/prepare_brand.py --src assets/brand/abyss_source.png --name abyss
```

## 8. Reglas que no se rompen

- No se recolorea la insignia a color (crema y verde son identidad).
- No se deforma ni se rota.
- No se pone sobre el tatuaje ni sobre el punto de mayor interes.
- Misma esquina y mismo tamano en toda la serie.
- Cero texto agregado a la foto: la insignia ya trae el nombre.
