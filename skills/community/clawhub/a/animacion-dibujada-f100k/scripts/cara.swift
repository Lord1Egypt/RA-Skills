// cara.swift — dónde están la cara, los ojos y la boca en una imagen (Vision de macOS, local y gratis).
// Coordenadas en pixeles de ESA imagen, origen arriba a la izquierda. Si hay varias caras, usa la más grande.
// Uso: swift cara.swift imagen.png  → imprime JSON:
//   { ancho, alto, cara: [x,y,w,h], ojoIzq: [x,y], ojoDer: [x,y], ojoAncho, boca: [x,y], bocaAncho, bocaAlto,
//     contornoOjoIzq: [[x,y]...], contornoOjoDer: [...], contornoBoca: [...] }   o   { ancho, alto, cara: null }
import Foundation
import Vision
import AppKit

guard CommandLine.arguments.count >= 2 else { print("uso: swift cara.swift imagen.png"); exit(1) }
let ruta = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: ruta), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
  print("No pude abrir la imagen: \(ruta)"); exit(1)
}
let W = Double(cg.width), H = Double(cg.height)
let req = VNDetectFaceLandmarksRequest()
do { try VNImageRequestHandler(cgImage: cg).perform([req]) } catch { print("Vision falló: \(error.localizedDescription)"); exit(4) }

func redondo(_ v: Double) -> Double { return (v * 10).rounded() / 10 }
let vacio: [String: Any] = ["ancho": W, "alto": H, "cara": NSNull()]
let caras = req.results ?? []
guard !caras.isEmpty else {
  print(String(data: try! JSONSerialization.data(withJSONObject: vacio), encoding: .utf8)!); exit(0)
}
var f = caras[0]
for c in caras { if c.boundingBox.width * c.boundingBox.height > f.boundingBox.width * f.boundingBox.height { f = c } }
let bb = f.boundingBox

func caja(_ r: CGRect) -> [Double] {
  let x = Double(r.minX) * W
  let y = (1.0 - Double(r.maxY)) * H
  let w = Double(r.width) * W
  let h = Double(r.height) * H
  return [redondo(x), redondo(y), redondo(w), redondo(h)]
}
func puntos(_ reg: VNFaceLandmarkRegion2D?) -> [[Double]] {
  guard let reg = reg else { return [] }
  var out: [[Double]] = []
  for pt in reg.normalizedPoints {
    let nx: Double = Double(bb.minX) + Double(pt.x) * Double(bb.width)
    let ny: Double = Double(bb.minY) + Double(pt.y) * Double(bb.height)
    out.append([redondo(nx * W), redondo((1.0 - ny) * H)])
  }
  return out
}
func centro(_ p: [[Double]]) -> Any {
  if p.isEmpty { return NSNull() }
  var sx = 0.0
  var sy = 0.0
  for q in p { sx += q[0]; sy += q[1] }
  return [redondo(sx / Double(p.count)), redondo(sy / Double(p.count))]
}
func ancho(_ p: [[Double]]) -> Double {
  if p.isEmpty { return 0 }
  var mn = Double.infinity
  var mx = -Double.infinity
  for q in p { mn = min(mn, q[0]); mx = max(mx, q[0]) }
  return redondo(mx - mn)
}
func alto(_ p: [[Double]]) -> Double {
  if p.isEmpty { return 0 }
  var mn = Double.infinity
  var mx = -Double.infinity
  for q in p { mn = min(mn, q[1]); mx = max(mx, q[1]) }
  return redondo(mx - mn)
}
let lm = f.landmarks
// Vision nombra los ojos desde el punto de vista de la persona: su ojo izquierdo queda a la DERECHA de la imagen.
var a = puntos(lm?.leftEye)
var b = puntos(lm?.rightEye)
if let ca = centro(a) as? [Double], let cb = centro(b) as? [Double], ca[0] > cb[0] { swap(&a, &b) }
let boca = puntos(lm?.outerLips)
let out: [String: Any] = [
  "ancho": W, "alto": H, "cara": caja(bb),
  "ojoIzq": centro(a), "ojoDer": centro(b), "ojoAncho": max(ancho(a), ancho(b)),
  "boca": centro(boca), "bocaAncho": ancho(boca), "bocaAlto": alto(boca),
  "contornoOjoIzq": a, "contornoOjoDer": b, "contornoBoca": boca,
]
print(String(data: try! JSONSerialization.data(withJSONObject: out), encoding: .utf8)!)
