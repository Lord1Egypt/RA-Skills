# Recorrido real con navegador

Solo aplica cuando la entrada es **código o una URL desplegada**. Con documento, el recorrido es mental
contra el texto (mismas 8 pruebas, buscando la frase que las resuelve).

**Herramienta:** la skill `agent-browser`. Es el motor por defecto para todo lo que sea navegador; entra con
sesión real y evita los muros que bloquean a un fetch pelado. No uses herramientas web genéricas para esto.

**Dónde guardar la evidencia:** capturas y notas a `informes/auditoria-ux/<app>/` del workspace, una carpeta por
auditoría. Cada hallazgo del informe apunta a su captura por nombre de archivo.

---

## Antes de tocar el navegador

1. **Levanta la app.** Lee el `package.json`: `npm run dev` salvo que el repo diga otra cosa. Ojo con el
   gestor de paquetes — hay repos que parecen usar pnpm y usan npm.
2. **¿Necesita variables de entorno?** Si faltan y la app no arranca, no inventes: audita el código y anota
   en "No verificado" que el recorrido no se pudo hacer y por qué.
3. **Si la app exige login y no lo tienes**, busca (o crea, si es barato) una ruta de previsualización que
   renderice el shell con datos falsos. En una de las apps de origen existía una ruta así y es lo que permitió medir el menú
   móvil sin sesión. Es la forma honesta de auditar el layout sin credenciales.
4. **Ten a mano dos identidades** si la app tiene cuentas: una con acceso y otra sin. La segunda es la que
   descubre la mitad de los hallazgos de la dimensión 9.
5. **Si llegar a las pantallas finales cuesta dinero** (una app que llama a un modelo de IA, consume
   créditos o gasta un cupo diario), **no las pagues para auditarlas**: inyecta el estado. Casi siempre la
   app guarda su progreso en `localStorage` con una forma conocida — escribe ahí una sesión sintética que
   incluya el caso que quieres ver (por ejemplo, un resultado a medias con algunos elementos fallidos) y
   recarga. Llegas al paso 4 sin gastar un centavo, y de paso pruebas casos que en un recorrido normal
   casi nunca ocurren.
   - Deriva la forma del objeto del esquema del código, no la adivines: si no valida, la app la descarta
     y creerás que el estado no se restaura.
   - **Marca los datos como sintéticos en tus notas.** Sirven para juzgar el layout y el flujo, nunca la
     calidad del contenido.
   - **Limpia al terminar.** Borra la clave y recarga: la app debe quedar como la encontraste.

---

## Las 8 pruebas

Corre las ocho, en este orden. Captura pantalla en cada una.

### P1 · Primera vez (estado vacío)
Entra sin datos: sesión nueva, o borra el almacenamiento local, o usa una cuenta recién creada.
- ¿La pantalla explica para qué sirve la app?
- ¿Hay un botón claro de la acción principal?
- ¿Hay un ejemplo de muestra, o te deja inventando el primer dato?

> Con almacenamiento local, `localStorage.clear()` y recarga. Con base de datos, cuenta nueva.

### P2 · Teléfono real (390px)
Redimensiona a **390×844** y repite el recorrido básico.
- **Abre el menú.** No basta con que la barra "se vea bien": la navegación tiene que poder abrirse.
- ¿Se usa con una mano? ¿Los botones se alcanzan con el pulgar?
- ¿Hay tablas que se cortan o textos que exigen zoom?
- Compara con 1280px: en escritorio debería verse el otro modo (barra completa, toggle oculto).

Mide los dos anchos, no solo el móvil. El bug clásico es que a un ancho se oculta una cosa y **nada** la
reemplaza (ver C10 en `cicatrices-produccion.md`).

> **Si el navegador no baja de cierto ancho** (en macOS, Chrome puede negarse a achicar la ventana por
> debajo de ~1500px): no abandones la prueba ni finjas que la hiciste. Estrecha el **contenedor** de la
> página por JavaScript al ancho interior real —`390 − padding lateral`, normalmente 358px— y mide ahí.
> **Solo vale como proxy si el componente no usa media queries internas**: revisa primero el código en
> busca de clases `sm:` / `md:` / `@media` en esa pantalla. Si las usa, el proxy miente y hay que probar
> en un teléfono físico. En cualquier caso, di en el informe con qué método mediste.

Lo que este proxy sí caza bien: rejillas de columnas fijas (`grid-cols-3` sin variante responsive) que
dejan celdas ilegibles, etiquetas de ancho fijo, y textos que se parten en cinco líneas.

### P3 · Refresco (no perder el trabajo)
Escribe algo, guárdalo, **recarga la página**.
- ¿Sigue ahí?
- Si no, es 🔴 y es el arreglo número uno, antes que cualquier detalle visual.
- Bonus: cierra la pestaña, abre de nuevo. Y en móvil, cambia de app y vuelve.

### P4 · Doble toque (duplicados)
Pulsa el botón de guardar **dos veces rápido**.
- ¿Se creó una fila o dos?
- ¿El botón se deshabilitó mientras procesaba?
- Guarda el mismo contenido dos veces por separado: ¿reemplaza o duplica?

### P5 · Silencio (feedback)
Toca cada botón de la pantalla principal y anota qué pasó visualmente.
- ¿Hubo estado de carga? ¿Confirmación?
- **Verifica que la confirmación sea cierta**: si dice "copiado", pega en algún lado; si dice "guardado",
  recarga y comprueba. Un éxito falso es peor que un error honesto.
- Provoca un error a propósito (desconecta la red, manda un campo vacío): ¿el mensaje se entiende?

### P6 · Vacío falso (la pantalla no miente)
Recorre cada pantalla que tenga contadores o resúmenes.
- ¿Algún contador dice un número mientras la lista de al lado dice "no hay nada"? Ese par es el bug.
- Pagina hasta el final de cada lista larga. Si el total cae exacto en 50, 100 o 1000, sospecha de un tope.
- Si algo sale vacío, mira la consola y la pestaña de red: un vacío que viene de una petición fallida es un
  error disfrazado, no un vacío.

### P7 · Sin permiso
Entra con la identidad que **no** tiene acceso (o cierra sesión y visita una URL protegida).
- ¿El mensaje dice por qué y qué hacer, o es un error rojo genérico?
- Si hay varias formas de entrar (llave, correo, Google), **prueba cada una** y compara qué datos ve cada
  una. Si ven cosas distintas, es la cicatriz C12 y es 🔴.
- Si hay pago: recorre pagar → desbloquear → usar, completo. El punto donde más rompe es justo después de pagar.

### P8 · Compartir
Copia el link público y ábrelo en una ventana privada, sin sesión.
- ¿Carga? ¿Se entiende sin que expliques nada?
- ¿Se ve decente al pegarlo en un chat (título y descripción)?
- Si la app embebe videos o documentos que alguien pegó a mano, comprueba que se reproduzcan y no salgan
  como recuadro roto.

---

## Mientras recorres, mira estas dos ventanas

- **Consola.** Filtra por errores. Un error de consola en la primera carga suele explicar un hallazgo visible.
- **Red.** Busca peticiones lentas (más de 2s) en el render inicial, y respuestas 3xx/401/404 que la app
  esté ignorando en silencio. El fallo que nadie ve es el que más dura.

## Cómo verificar un arreglo (no basta con escribirlo)

Después de aplicar cada arreglo 🔴, **re-corre la prueba que lo detectó** y captura de nuevo. El informe final
lleva las dos capturas, antes y después.

Si el arreglo va a producción y quieres confirmar que el código nuevo está sirviéndose de verdad: baja la
página con un cache-buster, saca el manifiesto de chunks, encuentra el nombre real del archivo y busca dentro
la propiedad que cambiaste — los nombres de propiedad de objetos no se minifican, las variables sí. Es el
método que sí sirvió para confirmar despliegues en la plataforma de cursos.
