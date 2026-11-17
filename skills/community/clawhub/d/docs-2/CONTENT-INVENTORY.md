# Inventario de contenido — SENDER

Fuente de verdad: [cristianoleamiranda-dotcom/sender](https://github.com/cristianoleamiranda-dotcom/sender) y las fichas publicadas en [sender.cl](https://www.sender.cl/). Nada de este sitio se inventó para llenar un hueco.

## Empresa

- Nombre: Sender
- Claim documentado: «Tecnología que transmite» / «Technology that transmits»
- Experiencia publicada: más de 20 años. No hay año de fundación.
- Teléfono: +56 9 8386 4148
- Correo: sender@sender.cl
- Ventas: bis.ltda@gmail.com
- Dirección: Blanco Viel 1108, 2º piso, San Miguel, Santiago, Chile
- WhatsApp: el mismo número, canal ya publicado
- No hay redes sociales publicadas. No se listan.

## Qué no está, y por eso no aparece

- Cifras de proyectos, clientes anónimos, certificaciones, premios, precios
- Fechas de hitos
- Coordenadas geográficas no publicadas
- Políticas legales no publicadas
- Rangos UHF numéricos (solo «enlaces UHF»)
- Telemetría en vivo. Una consola con números sería una simulación; no se simula.

## Catálogo

7 estaciones, 16 productos, especificaciones copiadas del catálogo auditado (`src/content/catalog.ts` del repo fuente). Cada ficha conserva `sourceUrl` hacia sender.cl.

## Proyectos

Seis instalaciones documentadas. Solo Radio Colosal, Ambato, tiene fuente de prensa (Radio World). El resto proviene de lo que Sender publica. No se asignan años.

## Imágenes

Solo archivos ya presentes en el repositorio fuente: `hero`, `hero-wide`, `about`, `cap-*`, `proj-am`, `proj-stl`, pósters WebP y `sender-hero.mp4`. No se generaron equipos, plantas ni personas nuevas. El texto alternativo describe el archivo; no afirma que una fotografía sea una instalación concreta si la fuente no lo dice.

## Idiomas

ES y EN son capas completas en `src/i18n/es` y `src/i18n/en`. El catálogo y los proyectos viven como pares `{ es, en }` para que una clave no pueda quedar sin traducción.

## SEO de partida

Títulos pedidos:

- ES: SENDER Chile | Ingeniería RF, Radiodifusión y Sistemas de Transmisión
- EN: SENDER Chile | RF Engineering, Broadcasting & Transmission Systems

Canónico de producción: https://www.sender.cl/
