# Luz, 3D y profundidad

Lo que hace que una foto plana se lea como una escultura fotografiada. Cada afirmacion
aqui esta implementada en `scripts/retouch.py` y es verificable mirando la etapa indicada.

## 1. El 3D no viene del contraste, viene del *sombreado*

Un objeto se lee tridimensional cuando la luminancia varia de forma **suave y
direccional** a lo largo de su superficie. El contraste global (una S fuerte) solo
separa blancos de negros: no crea volumen. El volumen viene de la componente de baja
frecuencia de la luz: el degradado.

Por eso `sculpture_3d()` trabaja sobre `blur(L, 5% del lado)` — el mapa de sombreado —
y no sobre el detalle. Es el mismo principio que usa un pintor: primero modela la forma
con un pincel grande, despues pone el detalle.

**Diagnostico practico:** si entrecerrando los ojos la imagen sigue viendose plana,
ninguna cantidad de nitidez la va a salvar. Falta modelado de gran radio.

## 2. La direccion de la luz manda

Todo el retoque de volumen es coherente con **una sola fuente**. En `dodge_burn()` la
luz clave esta en `key_light = (0.34, 0.24)` — arriba a la izquierda —. Si se ilumina
un lado y se sombrea el mismo lado, el cerebro lee "plastico".

Reglas de lectura:
- La luz clave define donde se hace *dodge* (brillar).
- La luz de relleno (o su ausencia) define donde se hace *burn*.
- El borde lejano del sujeto pierde luz: ahi va el burn perimetral que lo separa del fondo.
- Si la foto no tiene direccion clara, **no se inventa una nueva**: se refuerza la que
  ya existe (por eso el dodge esta limitado por `smoothstep` sobre la luminancia real).

## 3. Separacion del fondo (el "pop")

Cuatro recursos, de mas a menos importante:

1. **Negro real detras del sujeto** (`black_density` + viñeteo). El ojo compara bordes,
   y un fondo a 0.02 contra un sujeto a 0.60 es una diferencia de 30:1.
2. **Burn perimetral** radial: el encuadre se oscurece hacia las esquinas.
3. **Burn de contacto**: pequenas sombras en las uniones (bajo el menton, entre dedos).
   Esto es oclusion ambiental; es lo que "asienta" el objeto y evita que flote.
4. **Bloom calido** en el borde iluminado: sugiere dispersion atmosferica entre sujeto y
   fondo, es decir, distancia focal real.

## 4. Brillos: por que "bloom" no es "brillo"

| Concepto | Que es | Como se ve mal |
|---|---|---|
| Brillo / luminosidad | nivel tonal alto | gris lavado, sin punch |
| Especular | reflejo puntual de la fuente | quemado a blanco puro sin forma |
| **Bloom** | difusion optica: la luz se derrama en el objetivo | velo generalizado, contraste muerto |
| **Halation** | re-exposicion en la base de la pelicula: halo **rojo-naranja** | halo en todas las zonas claras, no solo especulares |

Investigacion (Kodak, Wikipedia *Film emulation*, guias de coloristas): el halo de
halation es calido **por estructura de la emulsion** — la capa roja esta mas cerca de la
base y recibe mas luz reflejada — y es **espacialmente selectivo**: aparece alrededor de
fuentes intensas contra zonas oscuras, no alrededor de cada camisa clara.

Implementacion: `bloom()` usa radios por canal `(1.22 R, 1.0 G, 0.82 B)` y limita el
efecto con `smoothstep(0.03, 0.22, L)` para que el negro del fondo no se levante. Si el
halo aparece por todos lados, se lee como plugin; si aparece solo en el borde iluminado,
se lee como optica.

## 5. Rolloff de altas luces (la firma filmica)

La curva caracteristica de la pelicula tiene **hombro** (shoulder) en las luces: los
tonos se comprimen gradualmente en lugar de recortarse en seco. Un sensor digital hace
lo contrario: mantiene detalle y despues corta.

`_shoulder(knee=0.66, c=2.2)` reproduce ese hombro: identidad hasta 0.66 y despues una
exponencial normalizada, C1-continua en el codo. Sin escalon no hay banding; con
pendiente decreciente no hay "plateau".

## 6. Clave baja: la trampa de la medicion

En una foto con 60% de fondo negro, el promedio de luminancia es ~0.06. Un algoritmo que
"normaliza el histograma" sube +1.5 EV y quema al sujeto. Es el error mas comun de los
presets automaticos y de los filtros de IA.

`meter_subject()` resuelve: descarta el fondo por umbral, mide el **p88 del sujeto** y lo
lleva a `key_tone` (0.60). La correccion se limita a ±0.55 EV y se aplica con curva
asintotica (`apply_exposure`), nunca con multiplicador lineal.

## 7. Textura: grano antes que nitidez

El grano cumple tres funciones: unifica transiciones (dithering natural contra el
banding), da microtextura donde no hay detalle real, y rompe la perfeccion digital.
Se modula por luminancia: casi nulo en negros (no ensucia el fondo) y reducido en luces.

El error opuesto es abusar del microcontraste: bordes duros + piel brillante = "IA
plastico". `micro_detail()` va atenuado en sombras y `sharpening()` tiene umbral para no
amplificar ruido.

## 8. Saturacion selectiva

La piel no es uniformemente saturada: los medios tonos son calidos, las sombras
profundas pierden croma. `sculpture_3d()` aplica `sat = 1 - 0.10*amount*(1-smoothstep(0,0.35,L))`
y `grade()` agrega micro-calidez solo entre 0.14 y 0.62 de luminancia. El resultado es
piel con sangre, no piel pintada.

## Tabla de sintomas → perilla

| Se ve... | Culpa de | Mover |
|---|---|---|
| Plano, sin relieve | falta de sombreado de gran radio | `sculpture` +0.10 |
| Lavado / gris | negros altos | `black_density` +0.06 |
| Quemado en bordes | exposicion lineal | `ev_limit` -0.15, `highlight_recovery` |
| Sucio / HDR | claridad excesiva | `clarity` -0.10 |
| Velo / niebla | bloom alto o sin piso | `bloom` -0.10 |
| Plastico | micro detalle + bloom | bajar ambos 30%, `grain` 0.03 |
| Frio / clinico | split toning o WB | `split_amount` -0.08 |
| Flota en el aire | falta oclusion | `burn` +0.08 |
