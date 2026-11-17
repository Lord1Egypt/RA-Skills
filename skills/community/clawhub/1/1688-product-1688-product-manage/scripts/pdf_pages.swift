import Foundation
import PDFKit

// Split only the requested pages so sips never silently renders just page one.
func fail(_ text: String) -> Never {
    FileHandle.standardError.write(Data(text.utf8))
    exit(2)
}
let args = CommandLine.arguments
guard args.count == 5,
      let first = Int(args[3]), let requestedLast = Int(args[4]),
      let document = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    fail("无法读取 PDF 或参数无效")
}
guard !document.isLocked, document.pageCount > 0 else {
    fail("PDF 加密或没有可读取页面")
}
let total = document.pageCount
let last = min(requestedLast, total)
guard first >= 1, first <= last else { fail("页码范围无效") }
var pages: [[String: Any]] = []
for number in first...last {
    guard let page = document.page(at: number - 1) else { fail("无法读取第 \(number) 页") }
    let single = PDFDocument()
    single.insert(page, at: 0)
    let path = URL(fileURLWithPath: args[2]).appendingPathComponent("page-\(number).pdf")
    guard single.write(to: path) else { fail("无法写出第 \(number) 页") }
    pages.append(["page": number, "path": path.path])
}
let result: [String: Any] = ["pageCount": total, "pages": pages]
let data = try JSONSerialization.data(withJSONObject: result, options: [.sortedKeys])
print(String(decoding: data, as: UTF8.self))
