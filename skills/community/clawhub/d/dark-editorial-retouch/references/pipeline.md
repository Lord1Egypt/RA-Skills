# Pipeline: que hace cada etapa y por que

Documento tecnico del motor `scripts/retouch.py`. Todo el procesamiento es en float32
(0..1) sobre arrays numpy: no hay perdida de precision entre etapas y no se sobrescribe
el original.

## 01. Lectura
`_load()` aplica `exif_transpose` (fotos de celular vienen rotadas por metadatos),
aplanan transparencias sobre negro y fuerzan RGB. HEIC de iPhone se soporta via
`pillow-heif` (registrado al importar).

## 02. Balance de blancos
Gray-world *robusto*: se toman solo pixeles de medios tonos (`0.18 < L < 0.85`) para que
un fondo negro dominante no arrastre la medicion hacia el cian. Las ganancias se
**clipean a ±8%**: un balance perfecto no vale si la piel deja de parecer piel. En
retoque editorial la dominante calida suele ser intencional.

## 03. Recuperacion de luces
`highlight_recovery()` actua **antes** de exponer. Si un canal supera 0.88 se reescala el
pixel completo (no el canal) para que la relacion de color sobreviva. Sin esto, al subir
la exposicion cualquier borde iluminado se convierte en un blob blanco sin informacion.

## 04. Medicion por sujeto
`meter_subject()` es la diferencia entre una foto bien expuesta y una reventada:

```
p05  = nivel del fondo (percentil 5)
thr  = max(p05 + 0.02, (p05 + p50) * 0.45)     # umbral que separa fondo de sujeto
key  = percentil 88 de la luminancia del sujeto
```

En clave baja el promedio del encuadre es ~0.06 (fondo negro = 60% del area). Si se
mide con ese promedio, el algoritmo "corrige" +1.5 EV y quema al sujeto. Midiendo el
p88 del sustrato contra `key_tone` (0.60) el resultado es estable en cualquier encuadre.

## 05. Exposicion protegida
Un multiplicador `rgb * 2**ev` es una ganancia lineal: en 0.6 EV las luces pasan de 0.9
a 1.35 y se recortan (plateau blanco). `apply_exposure()` usa en cambio:

```
salida = 1 - (1 - entrada) ** 2**ev      (para EV > 0)
```

Es una curva asintotica: levanta medios y sombras, y deja las luces altas casi quietas.
Equivale a mover "Sombras/Medios" en lugar de "Exposicion".

## 06. Curva de tono filmica
Tres piezas sobre la luminancia:

1. **S-simetria** `x*x*(3-2x)` mezclada con la identidad en `contrast * 1.35`.
   Contraste sin desplazar el punto medio (no oscurece la pieza).
2. **Pie denso**: resta proporcional por debajo de 0.30 → el fondo negro llega a 0.008
   sin empastar el detalle de las sombras del sujeto.
3. **Rodilla de altas luces** `_shoulder(knee=0.66, c=2.2)`: exponencial negativa
   normalizada, C1 en el codo. La pendiente decae de 1 a ~0.3 hasta el blanco. Esto es
   lo que evita el "plateau" y da el rolloff de pelicula.

## 07. Claridad local
Unsharp de radio grande (`3%` del lado menor) pero **con mascara de bordes**: solo
actua donde hay estructura (`|blur(L, s/2) - L|`). Las superficies lisas (fondo, pared)
no reciben nada, evitando el aspecto "HDR sucio".

## 08. Escultura 3D (el corazon del look)
```
shade  = blur(L, 5% del lado)          # mapa de sombreado de gran radio
relief = softlight(shade, shade*1.35 - 0.175) - shade
L'     = L + relief * sculpture * 1.6
```
Se toma la version difusa de la luminancia, se le aplica un contraste en S alrededor del
gris medio y se reinyecta **solo la componente de modelado**. Efecto: los volumenes
(antebrazo, cuero cabelludo, nudillos) ganan redondez sin tocar el detalle fino. Es el
equivalente matematico de un *matcap* tonal y la razon por la que el brazo "sale" del
fondo. Incluye desaturacion progresiva de sombras (piel real no es saturada abajo).

## 09. Dodge & burn
Tres mascaras:
- **Luz clave** eliptica en `key_light` (x, y relativos), limitada por
  `smoothstep(0.10, 0.55, L) * (1 - smoothstep(0.66, 0.92, L))`: ilumina lo que ya tiene
  luz y **no empuja lo que ya esta alto**.
- **Burn perimetral** radial: hunde el borde del encuadre para separar al sujeto.
- **Burn de contacto**: micro sombras donde el gradiente es alto y el tono bajo, lo que
  asienta el objeto (efecto oclusion).

Todo se aplica sobre luminancia y se reinyecta con `_apply_luma`, asi no hay corrimiento
de color (el defecto clasico de las herramientas Dodge/Burn nativas).

## 10. Bloom / brillos
```
hi    = smoothstep(0.62, 1.0, L)      # rodilla: nada por debajo de 0.62
glow  = blur(rgb*hi, r) *0.65 + blur(rgb*hi, 2.6r) *0.35
salida = screen(rgb, glow * tinte_calido, bloom)
```
Dos radios (halo corto + halo amplio) simulan la dispersion optica del objetivo. El
tinte calido (1.0, 0.94, 0.86) convierte el halo en "fuente incandescente". Un piso
`smoothstep(0.03, 0.22, L)` impide que el bloom levante el negro del fondo, que es el
error que arruina el contraste.

## 11. Micro detalle, grade, grano, marca
- **Micro detalle**: pasa-alto de radio minimo (`0.35%`), atenuado en sombras
  (`keep = 0.10 + 0.90*smoothstep(0.10,0.55,L)`). Devuelve textura de tinta y poro.
- **Grade**: split toning solo en medios tonos (negros neutros), vibrancia inversa a la
  saturacion, y micro-calidez de piel limitada a `0.14 < L < 0.62`.
- **Grano**: gaussiano, suavizado a sigma 0.8, modulado para no ensuciar negros ni
  luces. Es lo que evita el aspecto "render digital".
- **Viñeteo**: radial suave (no circular duro) `smoothstep(0.28, 0.95, r)`.
- **Marca**: ver `logo-integration.md`.

## Costos medidos (CPU, imagen 768x1376)

| Etapa | Tiempo |
|---|---|
| cadena completa sin marca | ~1.9 s |
| + marca (scrim, halo, sombra) | +0.4 s |
| lote de 12 fotos | ~30 s |

El cuello de botella son los `gaussian_filter` de radio grande; si se necesita mas
velocidad, se puede bajar la resolucion de trabajo y re-aplicar solo el grano y el
enfoque a resolucion final.
