# Lectura "motion design" aplicada a una imagen fija

Un fotograma de motion design no es una foto con filtro: es una imagen que **sugiere
tiempo**. Se diseña como si fuera el frame 1 de una animacion que el espectador completa
mentalmente. Estos son los recursos trasladables al still y como estan implementados.

## 1. Profundidad de campo por capas

En video, el sujeto esta separado del fondo por desenfoque, no solo por luz. En still:
el fondo debe ser una masa tonal sin bordes reconocibles. Regla: si el fondo tiene
detalle comparable al sujeto, se baja `clarity` y se sube el burn perimetral antes de
pensar en blur artificial.

## 2. Contraste por planos, no por pixeles

El frame se organiza en 3 planos tonales: fondo (0.00-0.05), plano medio (0.15-0.45),
sujeto (0.45-0.75). Un histograma con tres grupos separados se lee como "puesto en
escena"; un histograma continuo se lee como "foto de celular".

`tone_curve()` + `black_density` crean esa separacion; `sculpture_3d()` mantiene el plano
medio con estructura para que no se convierta en una mancha.

## 3. Foco de atencion unico

Motion design tiene un solo punto de maxima luminancia por frame (el "hero"). Se logra
con la mascara de luz clave: un unico gradiente calido, todo lo demas subordinado. Dos
focos con la misma intensidad rompen la jerarquia.

## 4. Micro-movimiento sugerido

Recursos que insinuan que la imagen "va a moverse":
- **Bloom/halation** en un borde: la luz esta entrando, algo va a pasar.
- **Grano** con densidad no uniforme: se lee como captura, no como render.
- **Viñeteo asimetrico** (la luz clave descentrada): composicion viva.
- **Lineas de fuga limpias**: encuadre que respeta un eje (el brazo vertical, por ejemplo).

## 5. Paleta restringida

Una paleta de 3 familias (negro, ambar de piel, hueso de la marca) es lo que hace que un
frame se lea "diseñado". El grade esta limitado a eso: `saturation` cerca de 1.0,
`vibrance` bajo, split toning con tinte de sombra casi neutro (`0.06, 0.09, 0.14`).
Cualquier color fuera de esas tres familias debe ser un accidente deliberado (un aro
dorado, un tatuaje rojo) y por eso vale.

## 6. Negros con textura, no negros muertos

Un negro a 0.000 es digital; un negro a 0.015 con grano es cine. `black_density` apunta
a 0.01-0.02 en el fondo, nunca a 0 exacto, salvo que se busque un corte grafico duro.

## 7. Movimiento implicito en el encuadre

Reglas practicas de composicion para feed vertical (4:5) y story (9:16):
- Sujeto en el tercio central; aire arriba para respirar.
- La marca ocupa una esquina inferior, alineada al margen del sujeto (no al borde del
  archivo): crea una linea invisible compartida.
- En 9:16 dejar 15% inferior libre: ahi van UI y captions de la plataforma.

## 8. Lo que NO se traslada

- Transiciones, keyframes, easing: no aplican. No se simulan con "lineas de velocidad"
  ni con blur direccional (es el atajo que grita "efecto de app").
- Titulos animados: si el pedido dice "sin textos", el frame queda solo con la marca.

## Checklist de "se siente motion"

- [ ] Un solo foco de luz, descentrado pero coherente.
- [ ] Tres planos tonales separados.
- [ ] Borde del sujeto con bloom calido, no con halo blanco.
- [ ] Fondo sin detalle reconocible y con grano.
- [ ] Marca en esquina, alineada a un margen interno.
- [ ] Ningun texto.
