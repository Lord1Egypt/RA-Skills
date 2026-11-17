# Leer el boceto y escribir los 3 prompts

El boceto no es una ilustración a mejorar: es un **plano de composición**. Dice qué objetos
van, dónde van y qué se mueve. Todo lo demás (material, luz, color) lo pone el estilo.

---

## 1. Inventario (antes de escribir un solo prompt)

Mira el boceto y escribe este bloque. Si algo no se entiende, va a **Dudas**, no se inventa.

```
LO QUE VEO
- Formato: vertical 9:16 / cuadrado / horizontal (si es horizontal, se recompone a 9:16 y se avisa)
- Vista: frontal plana / 3/4 / cenital / perfil
- Objetos (con su posición en tercios: arriba-izq, centro, abajo-centro…):
  1. …
  2. …
- Texto manuscrito (LITERAL, letra por letra): "…"
- Movimiento que ya trae el dibujo: flechas, líneas de velocidad, abanicos, rayos, trazos
  repetidos, un objeto a medio caer, algo desbordando
- Dudas: …
```

Reglas del inventario:

- **Cuenta los objetos.** Si hay 9 íconos, el prompt dice nueve y los nombra uno por uno, por
  fila. «Varios íconos» produce 5 o 14.
- **Nombra la forma dibujada, no la idealizada.** Si el robot es una caja con antena de bola,
  es «robot de caja con antena de bola», no «robot».
- **El texto se copia exacto.** Un texto mal escrito en la imagen quema el clip entero.
- **Máximo UNA pregunta.** Si la duda no cambia el movimiento, decide tú y dilo en una línea.

---

## 2. El ancla: ¿el boceto es el PRINCIPIO o el FINAL?

Aquí la skill original se equivoca: siempre toma el boceto como primer cuadro. Pero la
mayoría de los bocetos dibujan el **momento cumbre**, la idea ya completa. En el reel de
referencia, el dibujo del cofre muestra los íconos **ya volando** y la animación **termina**
calcando el dibujo.

| El dibujo muestra… | Ancla | El otro cuadro se saca… |
|---|---|---|
| La idea ya pasando: algo desbordando, saliendo, rompiéndose, envuelto, cayendo | **FINAL** | **restando**: el cofre cerrado, el edificio sin tentáculos, la gráfica plana |
| Un estado quieto con flechas que dicen qué va a pasar | **INICIAL** | **sumando**: lo que las flechas prometen, ya ocurrido |
| Dos viñetas (antes → después) | **AMBOS** | cada viñeta es un cuadro |

**Por qué importa:** el cuadro ancla es el que se parece al boceto. Si el boceto es el final y
lo pones de inicio, la animación arranca con la idea ya contada y **no hay recompensa**: el
movimiento se come la sorpresa.

Declárala en una línea: *«Ancla: FINAL. El dibujo ya muestra las ideas saliendo; el inicio es
el cofre cerrado y quieto.»*

---

## 3. El contrato de los dos cuadros

Los dos cuadros son **la misma toma en dos momentos**. Antes de escribirlos, fija una vez:

- Objetos y su apariencia
- Fondo
- Cámara (vista, altura, encuadre)
- Luz y paleta
- Estilo (bloque completo de `estilos.md`, copiado igual en los dos)

Lo único que cambia es **el delta**. Y el delta tiene que ser **legible**: «cerrado → abierto,
con los nueve íconos ya arriba» y no «se ve más dinámico».

**Cómo se consigue en la práctica:** el segundo cuadro NO se genera desde cero. Se genera
**editando el primero** (se le pasa como referencia con «edit this exact image, change only…»).
Dos generaciones independientes con el mismo texto dan dos tomas distintas y el video se
deforma intentando unirlas.

---

## 4. Plantillas

Los prompts van en **inglés** (los modelos obedecen mejor). Lo que le explicas al usuario va en
español.

### Cuadro ancla (con el boceto como referencia)

```
Use the attached hand-drawn sketch as a strict composition guide: keep every object, its
position, its relative size and the camera angle exactly as drawn. Do not add or remove
objects.

A vertical 9:16 [STYLE NAME] image. [STYLE BLOCK copied whole from estilos.md].

Composition, as in the sketch: [objeto 1 con posición]. [objeto 2 con posición]. …
[Si hay texto:] The only text in the image is "[TEXTO LITERAL]", in [tipo de letra], placed
[posición]. No other text, letters or logos anywhere.

State: [el momento que representa este cuadro, concreto].
```

### Cuadro opuesto (editando el ancla)

```
Edit this exact image. Keep the style, background, lighting, camera angle, framing, colors
and every object's design identical. Change ONLY this: [el delta, concreto y físico].
[Qué desaparece / qué se cierra / dónde queda cada objeto que se movió].
Everything not mentioned stays pixel-identical.
```

### Movimiento (para el video)

Una o dos frases. **No** vuelve a describir la imagen: describe **qué pasa, en qué orden, a
qué ritmo y qué hace la cámara**.

```
[Qué se mueve primero], then [qué sigue], [velocidad: snaps / eases / bursts / drifts].
[Detalle secundario que da vida: brillo, polvo, trazos que se arrastran]. Camera: [static /
very slow push in]. [Qué queda quieto: text and base stay locked]. No new objects appear.
```

Ejemplo real (el del reel, reescrito): *«The folder lid snaps open like paper, then the nine
cutout icons burst up and outward along the widening beams, speeding up as they spread. The
beams brighten slightly. Very slow push in, gentle stop-motion texture; the caption stays
locked at the bottom. No new objects appear.»*

---

## 5. Los 4 bocetos del reel, decodificados

Sirven para aprender a leer la **mecánica**; no son temas para copiar.

| Boceto | Idea (metáfora) | Ancla | Delta | Estilo que usó |
|---|---|---|---|---|
| Cabeza de perfil con un cerebro y un triángulo marcado | «eso pasa dentro de tu cabeza» | — (el reel no muestra el arranque) | un triángulo azul que vive dentro de un retrato real | foto de estudio + elemento gráfico |
| Edificio clásico (banco) con tentáculos | «algo se come a la institución» | FINAL | tentáculos rojos enrollándose hasta cubrir el edificio | collage retro (grabado + rojo) |
| Tarjeta «$1,000 ad» con gráfica que cae | «el anuncio pierde plata» | FINAL | la tarjeta azul arranca vacía y la línea se dibuja cayendo | editorial oscuro (azul sobre negro) |
| Carpeta abajo, rayos en abanico, 9 íconos | «tu bóveda de ideas» | FINAL | carpeta cerrada → abierta, íconos saliendo | miniatura 3D suave |

Patrón: **un solo objeto protagonista + una sola acción física**, y en los 3 que se ven completos el dibujo es el FINAL.
Ningún boceto tiene dos acciones. Si el del usuario tiene dos, son dos clips.

---

## 6. Sin boceto: de la frase del guion al dibujo

Si el usuario trae una frase del guion y no un dibujo:

1. Busca la **metáfora física** de la frase: un objeto + una acción. «El algoritmo se come tu
   alcance» → «un pulpo que envuelve tu vitrina». Propón 3, cada una en una línea.
2. El boceto lo hace el usuario, no tú: descríbeselo en 3 renglones para que lo haga en papel en 60 segundos
   (el dibujo real es lo que hace funcionar el split: la gente comenta porque ve SU trazo).
3. Si no quiere dibujar, pasa directo a los prompts sin ancla de boceto y **no uses los modos
   `split` ni `revelado`**: no hay boceto que mostrar, y uno generado por IA presentado como
   dibujo a mano es mentirle a la audiencia.
