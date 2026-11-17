# Rúbrica de UX de producto — 10 dimensiones

Cada dimensión vale **10 puntos**. Total 100. Puntúa solo lo que verificaste; lo no verificado se
anota aparte y **no suma ni resta** (dilo en el informe: "puntaje sobre 80 verificables").

Cómo puntuar cada dimensión, rápido:
- **10** — cumple todo, verificado.
- **7** — cumple lo esencial, falta un caso.
- **4** — existe la intención pero está a medias.
- **0** — no existe.

---

## 1. Claridad y un solo trabajo

**Pregunta:** ¿se entiende para qué sirve en 5 segundos, y hay UNA acción que manda?

**Ítems**
- [ ] En la primera pantalla hay una frase que dice para qué sirve.
- [ ] La app hace un trabajo, no cinco. La versión 1 no tiene 6 secciones en el menú.
- [ ] Hay **una sola acción primaria** por pantalla, visualmente distinta (color de acento, tamaño).
- [ ] Las acciones secundarias están en gris, texto o menú — no compiten.

**Prueba:** mira la pantalla entrecerrando los ojos. ¿Salta un solo botón, o hay cuatro iguales?
Si hay dos botones del mismo tamaño y color, uno de los dos no es el principal: bájalo de rango.

**Malo:** cuatro botones idénticos *Guardar · Compartir · Duplicar · Exportar*.
**Bueno:** *Guardar* en color; *Compartir* y *Duplicar* como texto pequeño al lado.

**Arreglo típico:** una acción primaria con el color de acento; el resto a `variant="ghost"` o a un menú
de tres puntos. Lo secundario que sobra en móvil se mueve a "Mi cuenta" antes que desbordar la barra.

---

## 2. Primer minuto

**Pregunta:** ¿alguien llega a "ah, qué útil" en menos de 60 segundos?

**Ítems**
- [ ] Se puede ver el valor **sin registrarse ni configurar**.
- [ ] Al abrir por primera vez ya hay algo dentro (2-3 datos de muestra, borrables), no una pantalla en blanco.
- [ ] Si hay onboarding: máximo 3 pasos, una pregunta por paso, "Paso 2 de 3" visible y **"Saltar" visible**.
- [ ] El onboarding **termina dentro de la app**, con el primer dato ya creado — no en una pantalla de "¡Listo!".

**Prueba:** cronométralo. Desde abrir hasta que sirvió de algo. Si pasa de 60 segundos, hay fricción de sobra.

**Los 3 tipos de onboarding y cuándo va cada uno**
| Tipo | Cuándo | Riesgo |
|---|---|---|
| **Sin onboarding** | La app hace una sola cosa y se entiende sola. Es lo mejor para una v1. | Si el valor no es obvio, la persona no sabe qué hacer. |
| **Tour de 3 pantallas** | El valor existe pero no se ve, o la app cambia un hábito. | Se vuelve catálogo de funciones. Máximo 3, una idea cada una. |
| **Onboarding de configuración** | La app necesita 2-3 datos para servir (nicho, meta, moneda). | Se convierte en formulario. Nunca más de 3 preguntas, todas salteables. |

**Arreglo típico:** datos semilla al primer arranque + mover el registro a después del primer resultado.

---

## 3. Los 4+1 estados

**Pregunta:** ¿cada pantalla está diseñada en sus cinco estados, no solo en "con datos"?

**Ítems**
- [ ] **Vacío** — explica el para qué + botón de la acción principal + 1 ejemplo de muestra.
- [ ] **Cargando** — esqueleto que ocupa el mismo espacio, no un "Cargando…" suelto que colapsa el layout.
- [ ] **Error** — dice qué pasó y qué puede hacer, en español, sin jerga técnica.
- [ ] **Con datos** — el caso feliz.
- [ ] **Sin permiso / bloqueada** — quien no pagó, no tiene acceso o está en otra cuenta entiende qué le pasa
      y cuál es el siguiente paso. (Este es el que falta en el 90% de las apps y el que más soporte genera.)

**Prueba:** borra todos los datos y mira la app. ¿Te invita a hacer algo o te deja plantada?
Luego entra con una cuenta sin acceso. ¿Sale un toast rojo genérico o una explicación?

**Malo:** "Sin resultados". · "No se pudieron cargar los detalles."
**Bueno:** "Aquí van los ganchos que te funcionan. Guarda el primero — o mira este de ejemplo." + botón + 1 tarjeta.

**Arreglo típico:** componente `EmptyState` reutilizable (frase + acción + ejemplo) y esqueletos con la
altura real de la fila. Para el estado 5, un mensaje por causa: no pagó / no inscrita / otra cuenta.

---

## 4. Feedback honesto

**Pregunta:** ¿la app nunca calla — y nunca miente?

**Ítems**
- [ ] Toda acción muestra respuesta inmediata: cargando → confirmación visible.
- [ ] El botón se deshabilita mientras procesa (si no, doble toque = doble guardado).
- [ ] Los mensajes de error se entienden sin ser técnica.
- [ ] **Ningún éxito falso**: si la operación no se completó, no aparece "¡Listo!".

**Prueba:** toca cada botón y pregúntate si la pantalla te confirmó algo. Después pulsa uno dos veces
rápido y mira si se duplicó.

**La trampa que ya te costó caro:** un `try {} catch {}` vacío alrededor de la operación mientras el toast
de éxito se dispara igual. La app dice "¡copiado!" y no copió nada. Ver `cicatrices-produccion.md` §Feedback.

**Arreglo típico:** que la función devuelva `true/false` de verdad y que el toast dependa de ese valor.
Nunca un `catch` vacío en un camino que muestra confirmación.

---

## 5. No pierde el trabajo

**Pregunta:** ¿cierro, vuelvo, y todo sigue ahí?

**Ítems**
- [ ] Guardado automático — sin botón de "guardar todo" que se pueda olvidar.
- [ ] Refrescar el navegador no borra nada.
- [ ] Guardar algo que ya existe lo **reemplaza**, no crea un duplicado.
- [ ] Si hay subida de archivos, el límite real coincide con el que promete la interfaz.

**Prueba:** llena la app, refresca. ¿Sigue todo? Si no, **este es el arreglo número uno**, antes que
cualquier detalle visual. Después guarda dos veces lo mismo y cuenta las filas.

**Arreglo típico:** `localStorage` en apps sin cuenta; upsert por clave estable (no por título) en apps con
base de datos; y un test que amarre el tope del cliente con el tope real del servidor.

---

## 6. La pantalla no miente

**Pregunta:** ¿lo que se ve corresponde a lo que hay?

Esta dimensión no está en los manuales: sale de tus propias apps. Es la clase de fallo más cara porque
la app **no parece rota** — parece vacía, y nadie reporta nada.

**Ítems**
- [ ] Ninguna lista dice "no hay nada" mientras un contador de la misma pantalla dice que sí hay.
- [ ] Ningún total está topado en silencio por un `limit` de la consulta.
- [ ] Ningún filtro esconde datos sin que exista la pantalla donde sí se ven.
- [ ] La pantalla que estás editando **es la que se monta** (cuidado con archivos muertos que parecen la app).
- [ ] Un fallo del servidor no se presenta como "vacío", se presenta como error.

**Prueba:** compara cada contador con la lista que tiene al lado. Si el resumen dice 6 y la lista dice
"no tienes ninguno", ahí está el bug. Y ordena o pagina hasta el final: si el total es exactamente 50,
100 o 1000, sospecha del tope.

**Arreglo típico:** que el fallo devuelva `null` (no un objeto vacío que parece dato válido); hidratar
desde el servidor **solo si viene con contenido**; paginar en vez de topar. Detalle en
`cicatrices-produccion.md` §La pantalla miente.

---

## 7. Móvil de verdad

**Pregunta:** ¿se usa con una mano, en un teléfono real?

**Ítems**
- [ ] A 390px de ancho, **la navegación existe y se abre**.
- [ ] Todo en una columna: nada de tablas anchas que se cortan.
- [ ] Botones grandes, textos legibles sin zoom.
- [ ] En pantalla grande la app solo se ensancha; el diseño nació en móvil.
- [ ] Si es PWA / se agrega a la pantalla de inicio: la sesión sobrevive ahí (iOS aísla las cookies del atajo).

**Prueba:** ábrela en tu teléfono real y úsala con una mano. Si tienes que hacer zoom o girar el teléfono,
falta trabajo. En navegador, viewport 390×844 y prueba **abrir el menú**.

**Malo:** una tabla de 6 columnas que en el teléfono se corta.
**Bueno:** cada fila se convierte en una tarjeta apilada, con el dato importante primero.

**Arreglo típico:** menú hamburguesa que de verdad esté renderizado (no solo previsto en el CSS), tabla →
tarjetas por debajo de `md`, y revisar el orden de las reglas CSS: a igual especificidad gana la última,
así que una regla base escrita **después** del `@media` lo anula a todo ancho.

---

## 8. Dashboard 1-3-5

Solo aplica si la app tiene pantalla de resumen. Si no la tiene, no restes: márcala **N/A** y reparte
sus 10 puntos proporcionalmente al resto.

**Ítems**
- [ ] **1 número héroe**: el dato por el que se abre la app. Grande, arriba, con su periodo al lado.
- [ ] **3 métricas de apoyo**, cada una con comparación (vs. la semana pasada, o cuánto falta para la meta).
- [ ] **5 filas de detalle** con su acción al lado, y un "ver todo". No cincuenta.
- [ ] Cada número lleva a una acción. Si no cambia nada de lo que vas a hacer, es vanidad: fuera.
- [ ] Héroe + apoyo + acción principal caben en la primera pantalla del teléfono, sin scroll.
- [ ] Los gráficos cuentan algo en una frase. Si no puedes decir qué muestra, sácalo.

**Malo:** "128". · Doce gráficos porque se ven profesionales.
**Bueno:** "128 esta semana · +19% vs. la anterior".

---

## 9. Puertas: acceso, cuentas y dinero

**Pregunta:** ¿entrar, pagar y desbloquear se entiende y no rompe?

Esta es la dimensión donde tus apps han sangrado más. No la audites solo leyendo: entra como alguien
que no tiene acceso.

**Ítems**
- [ ] **Una identidad, una cuenta.** Si hay dos formas de entrar (llave y correo, Google y magic link),
      ambas llevan a los MISMOS datos. El identificador de la cuenta no se deriva de la credencial.
- [ ] **El gate es coherente entre lista y detalle.** Si puedes ver algo en la lista, puedes abrirlo.
- [ ] **Después de pagar, funciona.** El camino completo (pagar → desbloquear → usar) se probó de punta a punta.
- [ ] **Si se cobra por uso**, un fallo al cobrar no tumba la operación que ya se hizo y ya costó dinero.
- [ ] **Los topes del plan están puestos a propósito**, no heredados de un valor por defecto que nadie miró.
- [ ] El enlace de acceso por correo sobrevive a los escáneres de seguridad (Outlook/Hotmail los pre-visitan).
- [ ] Quien queda bloqueada ve **por qué** y **qué hacer**, no un error genérico.

**Prueba:** crea una cuenta nueva por cada camino de entrada que exista y compara si ven lo mismo.
Después entra con una cuenta sin acceso y lee lo que dice la pantalla.

**Arreglo típico:** ver `cicatrices-produccion.md` §Puertas — están los cinco fallos reales con su fix.

---

## 10. Salir al mundo

**Pregunta:** ¿se puede mostrar, compartir y entender sin que tú expliques?

**Ítems**
- [ ] Tiene link público, nombre decente, y se ve bien al pegarlo en WhatsApp o Instagram (título + descripción).
- [ ] Alguien la abrió sin que le explicaras nada y la entendió.
- [ ] Los enlaces que pegan los humanos (Drive, YouTube, Loom) **se reproducen**, no salen como recuadro roto.
- [ ] Todo el texto visible está en español neutro, sin voseo ni jerga técnica.

**Prueba:** manda el link a alguien y mira si lo abre y lo entiende sin ayuda.

**Malo:** "te la muestro en videollamada porque solo funciona en mi computadora".
**Bueno:** `tuapp.vercel.app` — se abre en cualquier teléfono y se explica sola.

---

## Los 6 errores que hunden una primera app

Úsalos como lectura rápida antes de entregar el informe. Si alguno aplica, va en los tres arreglos de arriba.

1. **Querer todo en la versión 1** — corta funciones hasta que la app se pueda construir en un día.
2. **Pedir login desde el día 1** — duplica el trabajo y espanta antes de que se vea el valor.
3. **No definir los estados** — solo pensaste la pantalla "con datos".
4. **Copiar un dashboard de empresa** — doce gráficos que nadie mira.
5. **Decir "hazla bonita"** — sin referencia ni paleta, sale lo genérico.
6. **Construir sin probar en el teléfono** — se rompe justo donde la va a ver la audiencia.

## Frases para pedir (se pegan tal cual)

Cada hallazgo cierra con una de estas. Las ocho primeras son textuales del artifact *Crea Tu Aplicación*:
están escritas para que una alumna las pegue sin traducir nada. Las dos últimas cubren las dimensiones que
no están en el artifact y salen de las cicatrices de producción.

| Dim | Frase |
|---|---|
| 1 | La app tiene UNA pantalla principal y UNA acción destacada. Todo lo secundario va en un menú discreto, no compitiendo con la acción principal. |
| 1 | En cada pantalla, una sola acción primaria con el color de acento. Las secundarias van en gris, texto o menú. |
| 2 | Nadie tiene que registrarse ni configurar nada para ver el valor. La app abre con datos de ejemplo y la acción principal lista para tocar. |
| 3 | Define el estado vacío de cada pantalla: frase que explica el para qué + botón de la acción principal + 1 ejemplo de muestra. |
| 4 | Cada acción muestra respuesta inmediata: estado de carga, confirmación visible y mensaje de error entendible en español. |
| 5 | Guarda todo automáticamente en el navegador (localStorage) para que al cerrar y volver mis datos sigan ahí. Sin login por ahora. |
| 7 | Diseña primero para teléfono: una columna, botones grandes, sin tablas anchas; en pantalla grande solo se ensancha. |
| 10 | Que quede publicada con un link público, con título y descripción decentes para cuando se comparta. |
| 6 | Cada contador tiene que coincidir con su lista: si un resumen dice que hay datos, la lista de al lado no puede decir que no hay nada. Y ningún total puede venir topado por el límite de la consulta. |
| 9 | Todas las formas de entrar tienen que llevar a los mismos datos, y quien no tenga acceso debe ver por qué está bloqueada y cuál es su siguiente paso — no un error genérico. |

## Patrones de apps que ya lo resolvieron

Para explicar un hallazgo con un ejemplo que la persona conoce:

| App | Lo que hace | Lo que se copia |
|---|---|---|
| Duolingo | Te deja empezar una lección antes de crear cuenta | Valor primero, registro después |
| Canva | Nunca muestra un lienzo vacío: abres y eliges plantilla | Estado vacío que enseña |
| Notion | Tu primer espacio llega con plantillas dentro | Datos semilla |
| Cal AI | Foto del plato → calorías en segundos | Un solo trabajo, resultado inmediato |
| WhatsApp | Reloj, check, doble check | Feedback de estado siempre visible |
| Instagram | El `+` manda en la pantalla | Una acción primaria por pantalla |
| Apple Salud | Un número héroe: los pasos de hoy | Regla 1-3-5 |
| Stripe | Cada número con su comparación | Un número sin contexto no dice nada |
| Things | Al terminar todo, te felicita | El vacío también comunica |
| Spotify | Abre y reanuda lo que escuchabas | La principal continúa, no reinicia |
