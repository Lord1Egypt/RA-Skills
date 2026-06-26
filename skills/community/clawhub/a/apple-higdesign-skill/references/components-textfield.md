# Text Input Components

> 来源：Apple HIG - Text Fields (2026)
> https://developer.apple.com/design/human-interface-guidelines/text-fields

## TextField

### 设计原则
- 使用描述性占位符文字说明输入内容
- 保持标签简洁（1-2 个词）
- 避免使用提示性文字作为标签
- 提供清晰的输入反馈

### 样式变体

| 类型 | 使用场景 |
|------|---------|
| Default | 一般文本输入 |
| Filled | 需要视觉强调时 |
| Outlined | 表单、设置页面 |

### 状态
- **Default** — 未聚焦
- **Focused** — 聚焦高亮
- **Filled** — 有内容
- **Error** — 验证失败
- **Disabled** — 禁用

### 实现（SwiftUI）

```swift
// 基础 TextField
TextField("Email", text: $email)

// 带图标
TextField("Search", text: $query)
    .textFieldStyle(.search)

// 密码输入
SecureField("Password", text: $password)

// 多行输入
TextEditor(text: $notes)
    .frame(height: 100)
```

### 实现（UIKit）

```swift
// UITextField
let textField = UITextField()
textField.placeholder = "Email"
textField.borderStyle = .roundedRect
textField.keyboardType = .emailAddress
textField.autocapitalizationType = .none

// Secure Text Field
let secureField = UITextField()
secureField.isSecureTextEntry = true

// UITextView
let textView = UITextView()
textView.isScrollEnabled = true
```

---

## SearchBar

### 设计规范
- 提供清除按钮（用户右滑或点击）
- 支持取消按钮（iOS）
- 自动大写/纠正在适当时禁用
- 搜索历史建议

### 实现（SwiftUI）

```swift
@State private var searchText = ""

List {
    // 搜索结果
}
.searchable(text: $searchText, prompt: "搜索")
```

### 实现（UIKit）

```swift
// UISearchBar
let searchBar = UISearchBar()
searchBar.placeholder = "搜索"
searchBar.searchBarStyle = .minimal
searchBar.delegate = self

// 实现 UISearchBarDelegate
func searchBar(_ searchBar: UISearchBar, textDidChange searchText: String) {
    // 搜索逻辑
}

func searchBarSearchButtonClicked(_ searchBar: UISearchBar) {
    searchBar.resignFirstResponder()
}
```

---

## TextEditor

### 使用场景
- 多行文本输入（评论、备注）
- 可变长度内容
- 需要格式时用 UITextView

### 实现（SwiftUI）

```swift
struct NoteEditor: View {
    @State private var noteText = ""

    var body: some View {
        TextEditor(text: $noteText)
            .frame(minHeight: 100)
            .font(.body)
    }
}
```

### 实现（UIKit）

```swift
import UIKit

class NoteTextViewController: UIViewController, UITextViewDelegate {
    private let textView = UITextView()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupTextView()
    }

    private func setupTextView() {
        textView.delegate = self
        textView.font = .preferredFont(forTextStyle: .body)
        textView.isScrollEnabled = true
        textView.backgroundColor = .systemBackground
        textView.textContainerInset = UIEdgeInsets(top: 12, left: 8, bottom: 12, right: 8)

        // iOS 16+ 去除默认背景
        if #available(iOS 16.0, *) {
            textView.textInputBackgroundColor = .clear
        }

        textView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(textView)

        NSLayoutConstraint.activate([
            textView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            textView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            textView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            textView.heightAnchor.constraint(greaterThanOrEqualToConstant: 100)
        ])
    }

    // UITextViewDelegate
    func textViewDidChange(_ textView: UITextView) {
        // 文字变化时更新 UI
    }
}
```

### 注意事项
- 设置最小高度避免视觉闪烁
- 考虑 placeholder 实现
- iOS 16+ 支持 .scrollContentBackground() 去除背景
