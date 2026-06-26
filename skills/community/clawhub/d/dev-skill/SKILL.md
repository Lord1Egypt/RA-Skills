---
name: dev-skill
description: Generate SwiftUI iOS application code from PRD documents. Use when a PRD document is available and needs to be transformed into a working iOS application with proper architecture, UI components, and data management. This skill receives input from prd-skill and automatically triggers qa-skill after code generation.
---

# Dev Skill - SwiftUI iOS Development Generator

## Overview

This skill transforms Product Requirements Documents (PRD) into fully functional SwiftUI iOS applications. It analyzes PRD requirements and generates production-ready code with proper architecture, UI components, data models, and business logic.

## Architecture Pattern

### MVVM Architecture
All generated code follows the Model-View-ViewModel pattern:

#### Model Layer
- Data models (structs conforming to Codable)
- Data persistence (Core Data or SwiftData)
- Network layer (URLSession or Alamofire)

#### ViewModel Layer
- Business logic and state management
- Data transformation and validation
- Service coordination

#### View Layer
- SwiftUI views with proper componentization
- Navigation stack management
- UI state binding

## Code Generation Workflow

### 1. PRD Analysis
- Parse PRD document for functional requirements
- Extract screen specifications and user flows
- Identify data models and relationships
- Determine required third-party integrations

### 2. Project Structure Generation
Create a complete Xcode project with:

```
ProjectName/
├── ProjectName.xcodeproj
├── ProjectName/
│   ├── Models/
│   │   ├── DataModel.swift
│   │   └── APIModels.swift
│   ├── ViewModels/
│   │   ├── MainViewModel.swift
│   │   └── [Feature]ViewModel.swift
│   ├── Views/
│   │   ├── ContentView.swift
│   │   ├── [Feature]View.swift
│   │   └── Components/
│   │       ├── ButtonStyles.swift
│   │       └── CustomViews.swift
│   ├── Services/
│   │   ├── APIService.swift
│   │   └── DataService.swift
│   └── Utilities/
│       ├── Extensions.swift
│       └── Constants.swift
└── ProjectNameTests/
    └── [Feature]Tests.swift
```

### 3. Core Components Generation

#### 3.1 Data Models
```swift
struct Task: Identifiable, Codable {
    let id: UUID
    var title: String
    var isCompleted: Bool
    var dueDate: Date?
    var category: String
    var priority: Priority
}

enum Priority: String, Codable, CaseIterable {
    case low, medium, high
}
```

#### 3.2 ViewModels
```swift
class TaskViewModel: ObservableObject {
    @Published var tasks: [Task] = []
    @Published var selectedCategory: String?
    
    private let dataService: DataService
    
    init(dataService: DataService = .shared) {
        self.dataService = dataService
        loadTasks()
    }
    
    func addTask(_ task: Task) { ... }
    func deleteTask(_ task: Task) { ... }
    func toggleCompletion(_ task: Task) { ... }
}
```

#### 3.3 SwiftUI Views
```swift
struct TaskListView: View {
    @StateObject private var viewModel = TaskViewModel()
    @State private var showingAddTask = false
    
    var body: some View {
        NavigationView {
            List {
                ForEach(viewModel.tasks) { task in
                    TaskRowView(task: task)
                }
                .onDelete(perform: deleteTask)
            }
            .navigationTitle("Tasks")
            .toolbar {
                Button(action: { showingAddTask = true }) {
                    Image(systemName: "plus")
                }
            }
            .sheet(isPresented: $showingAddTask) {
                AddTaskView()
            }
        }
    }
}
```

### 4. Feature Implementation

#### 4.1 Navigation
- TabView for main navigation
- NavigationStack for hierarchical navigation
- Sheet presentations for modal views

#### 4.2 Data Persistence
- Core Data for complex relationships
- @AppStorage for simple preferences
- FileManager for document storage

#### 4.3 Networking
- Async/Await for modern API calls
- Error handling with Result type
- JSON decoding with Codable

#### 4.4 UI/UX
- Adaptive layout for all device sizes
- Dark mode support
- Accessibility features
- Haptic feedback

## Example: Todo App from PRD

**PRD Input:** Todo app with categories, reminders, sharing

**Generated Code:**
1. **Models**: Task, Category, Reminder
2. **ViewModels**: TaskListViewModel, CategoryViewModel
3. **Views**: TaskListView, CategoryView, AddTaskView, SettingsView
4. **Services**: NotificationService, SharingService
5. **Features**: 
   - Push notifications for reminders
   - Share sheet integration
   - iCloud sync for data
   - Widgets for quick access

## Auto-Trigger Next Steps

After generating the iOS project, this skill automatically:
1. Creates a complete Xcode project in `dev-output/` directory
2. Verifies code compiles without errors
3. Triggers `qa-skill` with the generated code as input
4. Provides build instructions and next steps

## Integration Requirements

### Input Format
- PRD markdown document from `prd-skill`
- Structured requirements with priorities
- Technical specifications and constraints

### Output Validation
- All code must compile in Xcode 15+
- Follows SwiftUI best practices
- Includes proper error handling
- Supports iOS 16+ deployment target

### Quality Standards
- 100% SwiftUI (no UIKit unless absolutely necessary)
- Proper separation of concerns
- Comprehensive documentation
- Follows Apple's Human Interface Guidelines