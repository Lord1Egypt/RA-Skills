# Cicatrices de producción — fallos reales de la app de guiones, la app de agencia, la plataforma de cursos, la app de retos y la app de escritorio con licencias

Cada uno de estos llegó a producción, lo sufrió alguien real, y costó tiempo encontrarlo. Son la parte
de la auditoría que un checklist genérico no tiene. Úsalos como **sondas**: por cada uno, corre el
chequeo. Si el chequeo da positivo, ya tienes un hallazgo con causa y arreglo listos.

> Todos están documentados con fecha y arreglo verificado. No los cites como "suele pasar": son hechos
> de estas apps. Si el mismo patrón aparece en otra app, dilo como *"mismo patrón que X"*, no como dato nuevo.

---

## §Feedback — la app que miente en verde

### C1 · El toast dice "¡copiado!" y no copió nada
**Dónde:** la app de agencia, botón "Copiar link del portal" (jul-2026).
**Causa:** `navigator.clipboard.writeText()` llamado **después** de un `await` de Server Action. El Clipboard
API async exige activación de usuario transitoria; tras el await se pierde y WebKit/Safari lanza
`NotAllowedError`. Estaba envuelto en un `try {} catch {}` vacío que se tragaba el error mientras el toast
igual anunciaba éxito.
**Chequeo:** busca `clipboard.writeText` y mira si hay un `await` antes en la misma función. Busca también
`catch {}` vacíos en funciones que muestran confirmación.
**Arreglo:** helper `copyToClipboard(text): Promise<boolean>` que intenta el API async y cae a `<textarea>`
oculto + `document.execCommand('copy')` (síncrono, no depende de la activación). Devuelve `true` solo si
copió de verdad; el llamador muestra `prompt(url)` como último recurso y **nunca** un toast de éxito falso.

### C2 · Guardar una imagen rompe la página entera (pantalla blanca)
**Dónde:** la app de agencia, logo de la agencia (31-jul-2026).
**Causa:** el archivo viaja como data URI dentro de un Server Action. El tope de body de los Server Actions
de Next es **1MB por defecto**, mientras la interfaz prometía 2MB. Dos números en dos archivos sin nada que
los amarre → `413 Body exceeded 1 MB limit` → sin `try/catch`, el fallo escala al error boundary global y
reemplaza la app entera por la pantalla blanca de error.
**Chequeo:** ¿hay subida de archivos por Server Action? Compara el tope del cliente con
`experimental.serverActions.bodySizeLimit` en `next.config`. ¿Existe `try/catch` en el handler del cliente?
**Arreglo:** subir `bodySizeLimit` (nunca por encima de 4.5MB, el tope de Vercel), `try/catch` en el cliente,
y un test que asserte `bodySizeLimit > tope_del_cliente`.
**Señal para el diagnóstico:** si alguien reporta *"la página entera se rompió al guardar algo"*, sospecha
un 413 de body antes que un bug de lógica.

### C3 · "NEXT_REDIRECT" en rojo en el formulario de login
**Dónde:** la app de agencia, `LoginForm.tsx` (jun-2026).
**Causa:** `redirect()` de una Server Action funciona **lanzando** un error especial que Next debe atrapar.
El `try/catch` del componente cliente lo capturó y lo pintó como error normal. La sesión sí se creó; la
usuaria quedó atascada en /login viendo una palabra técnica.
**Chequeo:** toda app Next con login/registro por Server Action + `redirect()` llamada desde un client
component con `try/catch`.
**Arreglo:** en el catch, detectar `digest`/`message` que empiece por `NEXT_REDIRECT` y **re-lanzarlo**.

---

## §La pantalla miente — vacío falso, totales topados, superficies muertas

### C4 · La lista dice "no hay nada" mientras el contador dice que sí hay
**Dónde:** la plataforma de cursos, pestaña Entregables del alumno. **Tres veces**: jul-4 (lista), jul-19 (Feedbacks),
jul-31 (filtro de fases). El resumen decía "6 Feedbacks recibidos" y la lista decía "no tienes ninguno".
**Causa:** el loader SSR, al fallar, devolvía `{ data: [] }` — un objeto **vacío pero truthy**. Ese valor
entraba como `initialData` de React Query con `staleTime` de 5 minutos → la librería lo trata como fresco y
**nunca reconsulta** → pantalla pegada en vacío que no se recupera sola. Las consultas sin `initialData` sí
funcionaban, por eso "Pendientes" traía datos y "Todos" no.
**Chequeo:** busca `initialData` en el código. Por cada uno, pregunta: ¿qué devuelve el loader cuando falla?
Si devuelve un array/objeto vacío en vez de `null`, es este bug.
**Arreglo:** hidratar desde el servidor **solo si viene con contenido** (`x?.length > 0 ? x : undefined`).
De fondo: que el `catch` del loader devuelva `null`, para distinguir "vacío por fallo" de "vacío real".
**Lección general que aplica a cualquier app:** un fallo que se presenta como vacío no se reporta como bug.
Se ve como una app que "todavía no tiene datos".

### C5 · El total miente y los datos se van a una pantalla que no existe
**Dónde:** la app de guiones, pestaña Guiones (jul-2026).
**Causa doble:** (1) la consulta del feed filtra `serie_id IS NULL` → asignar una serie a un guion lo **saca**
de Guiones; si la pestaña Series no está montada, el guion desaparece sin dónde verse (28 capítulos
invisibles). (2) La misma consulta tiene `limit=50` → el "TOTAL" muestra máximo 50 aunque haya más.
**Chequeo:** por cada contador de la interfaz, encuentra la consulta que lo alimenta y mira si tiene `limit`
o un `where` que excluya filas. Si el total es exactamente 50, 100 o 1000, es tope, no dato.
**Arreglo:** contar con una consulta de conteo aparte (sin `limit`), y garantizar que todo filtro que saca
datos de una vista tenga la vista de destino montada y alcanzable.

### C6 · Estás editando un archivo que no se monta
**Dónde:** la app de guiones. Un componente de app completo era **código muerto**; el shell vivo estaba en otra carpeta
y el router de pantallas en un tercer archivo.
**Chequeo:** antes de reportar "la pantalla X no tiene estado vacío", confirma que el archivo de la pantalla
X está importado en la cadena que arranca en la ruta. Un `grep` del nombre del componente basta.
**Por qué importa en una auditoría:** un hallazgo sobre un archivo muerto es un hallazgo falso, y un arreglo
sobre un archivo muerto es trabajo perdido que además parece hecho.

### C7 · El análisis sale falseado porque la consulta corta en 1000
**Dónde:** la app de retos, ranking del reto (jul-2026). La primera lectura mostraba a la participante
equivocada en 1º y alcance en 0 para todas.
**Causa:** PostgREST corta en **1000 filas** aunque pidas un `limit` mayor.
**Chequeo:** cualquier pantalla de ranking, métricas o exportación que lea más de 1000 filas sin paginar.
**Arreglo:** paginar con `offset`.

### C8 · El portal da 404 con cualquier token válido
**Dónde:** la app de agencia, Portal del Cliente (jul-2026).
**Causa:** el `select` pedía una columna que no existe en la tabla (`instagram`; el dato vive en
`social_links` JSONB). PostgREST rechaza el SELECT → `maybeSingle()` devuelve `data = null` → la ruta
interpreta "no encontrado" y lanza 404. El escritor del token sí funcionaba, así que el link se generaba
bien y el portal fallaba después: parecía problema de token.
**Chequeo:** en rutas por token/slug, compara las columnas del `select` real contra el esquema. Y revisa si
el test de esa ruta selecciona las **mismas** columnas que la función real — si el test hace `.select('id')`,
no caza el drift de esquema.
**Arreglo:** seleccionar las columnas que existen. En tests de rutas por token, replicar el select real.

---

## §No pierde el trabajo

### C9 · "Actualizar" crea un duplicado
**Dónde:** la app de guiones, la acción de guardar guion (jul-2026). Rehacer 21 guiones dejó **42 entradas**.
**Causa:** la operación de guardado **siempre inserta**, aunque el título sea idéntico. No hace upsert, y no
existía herramienta de borrado → la limpieza es manual.
**Chequeo:** guarda dos veces lo mismo y cuenta las filas. Revisa si hay una clave estable para el upsert.
**Arreglo:** upsert por una clave estable (id), no por título. Y si el camino de escritura no tiene update ni
delete, esa ausencia es un hallazgo 🔴 por sí sola: una app donde no se puede corregir obliga a acumular basura.

---

## §Móvil de verdad

### C10 · En el celular no aparece ninguna opción
**Dónde:** la app de guiones, `TopNav.tsx` (jul-2026).
**Causa:** en `≤760px` el CSS ocultaba las pestañas esperando un `.app-nav-mobile-toggle` que el componente
**nunca renderizó** (una tarea quedó a medias). Resultado: en el teléfono no había navegación en absoluto.
**Gotcha CSS que lo hacía invisible incluso al arreglarlo:** las reglas base estaban escritas **después** del
`@media`. A igual especificidad gana la última en orden de fuente, así que la base anulaba el media query a
todo ancho y el toggle nunca podía mostrarse. Un `@media` **no añade especificidad**.
**Chequeo:** viewport 390px y **abre el menú**. Si el CSS oculta algo en móvil, confirma que existe el
elemento que lo reemplaza y que su regla base está **antes** del `@media`.
**Arreglo:** renderizar el toggle + panel con todas las pestañas; mover el cluster secundario (tema, fuente,
selector de cuenta, campana) a "Mi cuenta" en vez de desbordar la barra.
**Cómo verificarlo sin login:** una ruta de previsualización que renderice el shell con datos falsos, y
medir a viewport CSS real: @390px toggle visible / tabs ocultas; @1280px al revés.

### C11 · Desde el atajo del iPhone no hay sesión (en Safari sí)
**Dónde:** la app de guiones, PWA (jul-2026).
**Causa:** con `display:standalone` + `appleWebApp.capable:true`, el ícono de pantalla de inicio en iOS es un
contenedor con **cookies aisladas**: el login se completa en Safari y la sesión nunca llega al atajo.
**Chequeo:** ¿la app es PWA y tiene login? Pregunta si alguien la usa desde el ícono del teléfono.
**Arreglo aplicado:** `appleWebApp.capable:false` → iOS abre el atajo en Safari, con cookies compartidas. Se
dejó el manifest en `standalone` a propósito: Android conserva modo app y share_target, y no tiene el bug.
**Detalle operativo:** hay que **borrar y volver a agregar** el atajo — iOS cachea el flag al momento de
"Añadir a inicio".

---

## §Puertas: acceso, cuentas y dinero

### C12 · El equipo se parte en silos sin ningún aviso
**Dónde:** la app de escritorio con licencias, sincronización de casos entre computadoras (jul-2026).
**Causa:** el silo de datos **era literalmente la llave de licencia canonicalizada**, y había **dos puertas
que reparten llaves distintas**: pegar la llave te da esa llave; entrar solo con el correo te da una llave
derivada del correo. Dos computadoras solo se sincronizan si se activaron por la misma puerta. Caso real: la
dueña de la cuenta en un silo y todo su equipo en otro, la misma persona con un caso
abierto en cada uno, y ninguno veía al otro.
**La trampa viva:** si una colaboradora entra con **su propio** correo y ese correo está autorizado, el
sistema la deja pasar **sin error** y la manda a un tercer silo en silencio.
**Chequeo:** enumera todas las formas de entrar. Por cada una, crea una cuenta y compara qué datos ve. Si el
identificador de la cuenta se deriva de la credencial, ya está roto.
**Lección general (la más importante de todo este archivo):** **cuando el identificador de la cuenta se
deriva de la credencial, cada forma nueva de autenticarse crea una cuenta nueva.** La cuenta tiene que ser
un dato propio, no un subproducto del login.
**Arreglo:** una columna de cuenta explícita a la que varias llaves puedan apuntar, editable desde el panel.

### C13 · Ve la lista pero no puede abrir el detalle
**Dónde:** la plataforma de cursos, entregables (jun-2026). Toast rojo: "No se pudieron cargar los detalles".
**Causa:** dos consultas con reglas de acceso distintas. La lista mostraba por programa sin exigir inscripción
activa; el detalle exigía `status = 'active'`. Cualquier estado distinto (invited, paused, completed, dropped)
veía la lista y chocaba en el detalle.
**Chequeo:** por cada par lista/detalle, compara literalmente las condiciones de acceso. Deben ser iguales o
la lista debe filtrar lo que el detalle va a rechazar.
**Arreglo:** igualar el gate. Y si un elemento no se va a poder abrir, no listarlo.

### C14 · Alumnas que se quedan a medio inscribir, y crece cada día
**Dónde:** la plataforma de cursos, onboarding de alumnas (jul-2026).
**Causa:** el plan tope traía un `maxStudentsPerProgram` heredado del valor por defecto — mucho más bajo que
la cantidad real de inscritas. El onboarding era una secuencia de 8 pasos **sin transacción**: el paso que
crea el perfil corría, el paso del tope lanzaba, y el paso que crea la inscripción nunca llegaba →
**huérfanas**: existen como alumnas pero sin inscripción, y no pueden abrir nada.
**Chequeo:** ¿hay topes de plan? ¿Alguien los puso a propósito? ¿El alta de usuario es atómica o es una
secuencia de pasos donde el fallo del paso 7 deja creado el paso 4?
**Arreglo:** quitar el tope heredado y volver el alta **atómica** (un procedimiento transaccional que cree
todo o nada), más el backfill de quienes ya quedaron a medias.
**Regla:** todo alta de usuario en varios pasos necesita transacción, o produce fantasmas que nadie ve hasta
que reclaman.

### C15 · 500 después de haber pagado el token de la IA
**Dónde:** la app de guiones, acción de créditos nueva (jul-2026).
**Causa:** agregar una acción de créditos a la tabla de costos **no basta**: la tabla del libro mayor tiene un
CHECK que enumera las acciones válidas. Una acción que no esté ahí viola la restricción, el procedimiento
lanza, y si la ruta no lo atrapa devuelve 500 **después** de haber pagado el token: el texto generado se
pierde y en la pantalla no pasa nada. Nunca funciona ni una vez.
**Chequeo:** agregar una acción de créditos toca **tres lugares**: la tabla de costos, el CHECK de la columna
en una migración nueva, y aplicar esa migración en producción antes de desplegar. Verifica los tres.
**Arreglo:** los tres lugares + envolver el cobro en `try/catch`. **Un fallo de cobro no debe tumbar una ruta
que ya generó y ya guardó material**: entrega con aviso y registra, o el reintento sale gratis infinitas veces.
**Por qué ninguna revisión por tarea lo cazó:** el defecto vive en la unión de dos archivos que ninguna tarea
tocaba a la vez. Solo apareció revisando la rama completa. Aplica igual a cualquier lista blanca duplicada
entre la base y la API.

### C16 · "El enlace no es válido o ha expirado" en Hotmail/Outlook
**Dónde:** la app de retos, enlace mágico de acceso (jul-2026). Solo correos de Hotmail/Outlook/corporativos.
**Causa:** el enlace es de **un solo uso**, y los escáneres de seguridad de correo **pre-visitan el enlace con
un GET apenas llega**, antes del clic humano. Como la verificación ocurría en el GET, el escáner quemaba el
token. Gmail no pre-escanea así de agresivo, por eso el bug parecía aleatorio.
**Chequeo:** ¿hay acceso por enlace de correo? ¿La verificación ocurre en el GET de la URL del correo?
**Arreglo:** el GET solo **muestra una página con un botón**; la verificación real ocurre en un POST tras el
clic humano. Los escáneres hacen GET, no envían formularios. (Depende de que la plantilla del correo apunte a
tu ruta propia; si apunta a la URL de verificación del proveedor, el fix no sirve.)
**Desbloqueo inmediato de una persona, sin desplegar:** asignarle contraseña y decirle que entre por esa vía.

### C17 · Reciclar una sesión bloquea a quien ya participó
**Dónde:** la app de retos, Pasaporte (jul-2026). Casi ninguna asistente pudo reclamar.
**Causa:** una restricción única `(sesión, participante)` impide reclamar dos veces la misma fila. Reabrir una
sesión vieja (cambiarle la ventana y el código) parece equivalente a crear una nueva y no lo es: quien ya
reclamó queda bloqueada con "ya reclamaste" y el muro no le suma.
**Chequeo:** ¿la interfaz ofrece "editar" sobre un registro que ya tiene participaciones? ¿Avisa?
**Arreglo:** la app ahora pide confirmación explícita cuando la edición mueve la ventana o el código sobre una
sesión con participaciones, y a la participante le dice **"lo reclamaste el 16 de julio"** en vez del genérico.
**Regla de UX:** un mensaje de bloqueo genérico sobre un caso legítimo convierte un dato en una queja.

---

## §Salir al mundo

### C18 · El video sale como recuadro roto
**Dónde:** la app de agencia, portal del cliente (jul-2026).
**Causa:** los editores pegan un enlace de **Google Drive** como video, y el portal hacía `<video src={...}>`.
Un `<video>` no reproduce enlaces de Drive ni de YouTube: Drive sirve una página HTML, no un archivo.
**Chequeo:** ¿algún reproductor recibe un enlace **pegado por un humano**? Ahí siempre llega Drive.
**Arreglo:** un resolvedor que devuelva `iframe | video | link` según el origen — Drive/Docs, YouTube
(watch/youtu.be/shorts/embed), Vimeo y Loom van a iframe con su URL de embed; archivo directo va a `<video>`;
desconocido cae a un botón "abrir en pestaña". Nunca `<video src>` directo sobre un enlace pegado.

### C19 · El portal tarda una eternidad en abrir
**Dónde:** la app de agencia, mismo portal.
**Causa:** el render hacía el scrape de Instagram (10-60 segundos) antes de mostrar nada.
**Chequeo:** ¿hay alguna llamada lenta a un tercero dentro del render de la primera pantalla?
**Arreglo:** sacarla del render y cargarla bajo demanda cuando se abre esa pestaña, con esqueleto.

---

## §Silencio operativo — lo que falla sin que nadie se entere

### C20 · Cinco semanas sin guardar nada, y el panel decía "ok"
**Dónde:** rutina automática que subía guiones a la app de guiones. Se rompió el 18 de junio; se descubrió el 23 de julio.
**Causa:** dos fallos apilados — el dominio se había movido (respondía **308** a la URL nueva, y al seguir el
redirect se descarta la cabecera de autorización al cambiar de host) y la llave estaba rotada (**401**). Pero
lo que lo hizo durar cinco semanas fue otra cosa: **la rutina hacía el POST y seguía adelante sin mirar el
código HTTP**, y el panel seguía marcando "ok".
**Chequeo:** toda rutina automática, cron o integración que escriba en otro sistema. ¿Verifica el status?
¿Propaga el fallo a algún lugar donde alguien lo vea?
**Arreglo:** el paso solo cuenta como exitoso con el status esperado y el cuerpo esperado; cualquier otra cosa
marca la rutina en error. **Un paso que falla en silencio es peor que uno que revienta.**

### C21 · "No se pudo generar" porque el modelo no existe
**Dónde:** la app de guiones, 4 rutas con su propio `fetch` a la API (jul-2026).
**Causa:** cada una tenía el nombre del modelo **con fecha, escrito a mano**, y esa versión no existe → 404.
Solo no explotaba porque la variable de entorno de producción lo sobrescribía.
**Chequeo:** busca nombres de modelo con fecha escritos a mano fuera de la librería central.
**Arreglo:** usar el alias sin fecha, que siempre resuelve a la última versión.

---

## §Números que engañan

### C22 · El ranking se rompió y la que iba ganando cayó al séptimo puesto
**Dónde:** la app de retos, un reto de comunidad, a mitad de camino (jul-2026). Verificado con datos de producción.
**Tres defectos a la vez:**
1. **Escala sin tope.** los puntos por crecimiento repartían tres veces más que la constancia de todas
   las participantes juntas: un solo corte pesaba más que todo el reto. Una cuenta muy grande sumó muchísimo por
   crecer menos de 1%; quien tenía ventas reales —el objetivo del reto— quedó séptima.
2. **Restar dos ventanas rodantes.** El alcance de Instagram es una ventana de N días, no un acumulado.
   Restar dos capturas no mide "lo generado durante el reto". Los seguidores sí son acumulado y esa resta vale.
   **Regla: nunca puntúes restando dos ventanas rodantes.**
3. **La instrucción no decía la ventana**, así que cada quien capturó un periodo distinto y casi un tercio quedó
   con delta negativo → cero puntos.
**Chequeo:** por cada número que la app calcula a partir de datos que la persona reporta, pregunta: ¿es un
acumulado o una ventana? ¿Tiene tope? ¿La instrucción dice exactamente qué capturar?
**Arreglo:** tope por evento, normalizar a base semanal cuando las ventanas difieren, y —la mejor decisión—
liquidar una sola vez al final, cuando las ventanas quedan contiguas sin solaparse.
