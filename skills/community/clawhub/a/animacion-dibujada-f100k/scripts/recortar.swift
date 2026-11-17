// recortar.swift — separa a la persona (o el sujeto principal) del fondo con Vision de macOS 14+.
// Gratis y local: es el mismo recorte de «Copiar sujeto» de Fotos. Sale un PNG con fondo transparente,
// recortado justo al borde del sujeto.
// Uso: swift recortar.swift foto.jpg salida.png
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else { print("uso: swift recortar.swift foto.jpg salida.png"); exit(1) }
// applyOrientationProperty: respeta la foto girada del celular (EXIF), si no sale acostada
guard let ci = CIImage(contentsOf: URL(fileURLWithPath: args[1]), options: [.applyOrientationProperty: true]) else {
  print("No pude abrir la foto: \(args[1])"); exit(1)
}
let req = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: ci)
do {
  try handler.perform([req])
  guard let obs = req.results?.first, !obs.allInstances.isEmpty else {
    print("No encontré ninguna persona ni objeto claro en la foto. Prueba con una donde el sujeto se separe del fondo."); exit(2)
  }
  let buf = try obs.generateMaskedImage(ofInstances: obs.allInstances, from: handler, croppedToInstancesExtent: true)
  let out = CIImage(cvPixelBuffer: buf)
  guard let cg = CIContext().createCGImage(out, from: out.extent) else { print("No pude armar el recorte."); exit(3) }
  let rep = NSBitmapImageRep(cgImage: cg)
  guard let png = rep.representation(using: .png, properties: [:]) else { print("No pude guardar el PNG."); exit(3) }
  try png.write(to: URL(fileURLWithPath: args[2]))
  print("recorte -> \(args[2]) (\(cg.width)x\(cg.height))")
} catch {
  print("Vision falló al recortar: \(error.localizedDescription)"); exit(4)
}
