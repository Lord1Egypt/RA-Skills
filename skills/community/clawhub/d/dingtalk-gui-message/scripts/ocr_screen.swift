#!/usr/bin/env swift
// ocr_screen.swift — 截图 OCR，输出 JSON 格式的文字+坐标
// 用法: swift scripts/ocr_screen.swift /path/to/screenshot.png ["搜索关键词"]

import Foundation
import Vision
import AppKit

guard CommandLine.arguments.count >= 2 else {
    let json: [String: Any] = ["success": false, "error": "用法: swift ocr_screen.swift <图片路径> [搜索关键词]"]
    if let data = try? JSONSerialization.data(withJSONObject: json),
       let str = String(data: data, encoding: .utf8) {
        print(str)
    }
    exit(1)
}

let imagePath = CommandLine.arguments[1]
let searchKeyword = CommandLine.arguments.count >= 3 ? CommandLine.arguments[2] : nil

guard let image = NSImage(contentsOfFile: imagePath),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    let json: [String: Any] = ["success": false, "error": "无法加载图片: \(imagePath)"]
    if let data = try? JSONSerialization.data(withJSONObject: json),
       let str = String(data: data, encoding: .utf8) {
        print(str)
    }
    exit(1)
}

let imageWidth = cgImage.width
let imageHeight = cgImage.height

let request = VNRecognizeTextRequest()
request.recognitionLanguages = ["zh-Hans", "zh-Hant", "en-US"]
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])

do {
    try handler.perform([request])
} catch {
    let json: [String: Any] = ["success": false, "error": "OCR 失败: \(error.localizedDescription)"]
    if let data = try? JSONSerialization.data(withJSONObject: json),
       let str = String(data: data, encoding: .utf8) {
        print(str)
    }
    exit(1)
}

guard let observations = request.results else {
    let json: [String: Any] = ["success": false, "error": "无 OCR 结果"]
    if let data = try? JSONSerialization.data(withJSONObject: json),
       let str = String(data: data, encoding: .utf8) {
        print(str)
    }
    exit(1)
}

var results: [[String: Any]] = []
var matchedResults: [[String: Any]] = []

for obs in observations {
    guard let candidate = obs.topCandidates(1).first else { continue }
    let text = candidate.string
    let bb = obs.boundingBox
    
    // Vision 坐标系：左下角为原点，归一化 0~1
    // 转换为图片像素坐标（左上角为原点）
    let pixelX = Int((bb.origin.x + bb.width / 2) * Double(imageWidth))
    let pixelY = Int((1.0 - (bb.origin.y + bb.height / 2)) * Double(imageHeight))
    let pixelLeft = Int(bb.origin.x * Double(imageWidth))
    let pixelTop = Int((1.0 - bb.origin.y - bb.height) * Double(imageHeight))
    let pixelWidth = Int(bb.width * Double(imageWidth))
    let pixelHeight = Int(bb.height * Double(imageHeight))
    
    let item: [String: Any] = [
        "text": text,
        "center_x": pixelX,
        "center_y": pixelY,
        "left": pixelLeft,
        "top": pixelTop,
        "width": pixelWidth,
        "height": pixelHeight,
        "confidence": candidate.confidence
    ]
    
    results.append(item)
    
    // 如果有搜索关键词，检查是否匹配
    if let keyword = searchKeyword, text.contains(keyword) {
        matchedResults.append(item)
    }
}

var output: [String: Any] = [
    "success": true,
    "image_width": imageWidth,
    "image_height": imageHeight,
    "total_items": results.count,
    "all_texts": results
]

if let keyword = searchKeyword {
    output["search_keyword"] = keyword
    output["matched"] = matchedResults
    output["match_count"] = matchedResults.count
}

if let data = try? JSONSerialization.data(withJSONObject: output, options: [.prettyPrinted]),
   let str = String(data: data, encoding: .utf8) {
    print(str)
}
