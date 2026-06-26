"""
Web Browser skill that sends text prompts to Perchance.org and displays the resulting images.

This script creates a web browser that can:
1. Take text prompts and send them to Perchance.org for image generation
2. Display the generated images in a web view
3. Support multiple image generation runs
4. Handle various error conditions gracefully
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QStandardPaths

# Add the script directory to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import requests


class WebBrowser(QMainWindow):
    """Main web browser class for displaying generated images"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Perchance Image Browser')
        self.resize(800, 600)
        self.setMinimumSize(800, 600)

        # Create the main view widget - QWebView requires QtWebEngineWidgets
        self.webView = QWebView()  # QWebView is from QtWebEngineWidgets, not PyQt5.QtWidgets
        self.setWebViewWidget(self.webView)
        
        self.setFixedSize(800, 600)

        # Add input fields and buttons
        self.prompt_label = QLabel("Enter prompt:")
        self.prompt_input = QLineEdit()
        self.prompt_input.setFixedWidth(400)
        self.prompt_input.setTextPlaceholder("Type a detailed prompt here...")
        self.prompt_input.returnPressed.connect(self.generate_image)

        self.num_images_label = QLabel("Images:")
        self.num_images_input = QLineEdit("1")
        
        self.orientation_label = QLabel("Orientation:")
        self.orientation_input = QLineEdit("landscape")

        self.submit_btn = QPushButton("Generate Image")
        self.submit_btn.setDefault(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.num_images_label)
        layout.addWidget(self.num_images_input)
        layout.addWidget(self.orientation_label)
        layout.addWidget(self.orientation_input)
        layout.addWidget(self.submit_btn)
        layout.addStretch()

        # Set layout
        self.setLayout(layout)

        # Add status message label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-weight: bold; color: blue;")
        self.setStatusBar(self.status_label)
        self.setStatusBarAlwaysActive = True

    def generate_image(self):
        """Generate an image from a text prompt"""
        try:
            # Get input values
            prompt = self.prompt_input.text().strip()
            num_images = int(self.num_images_input.text()) if self.num_images_input.text().strip() else 1
            
            if not prompt:
                QMessageBox.critical(self, "Error", "Please enter a prompt")
                return

            if num_images < 1:
                QMessageBox.warning(self, "Warning", "Please enter at least 1 image")
                return

            orientation = self.orientation_input.text().strip() or "landscape"

            if num_images == 1:
                QMessageBox.information(self, "Single Generation", f"Generating image {1}/{num_images}...")
            else:
                for i in range(num_images):
                    self.webView.load(QUrl("about:blank"))
                    self.status_label.setText(f"Generating image {i+1}/{num_images}...")
                    
                    # Small delay between generations
                    import time
                    time.sleep(0.1)

                    # Generate the image
                    self.webView.load(QUrl("about:blank"))
                    self.status_label.setText(f"Image {i+1}/{num_images}...")
                    time.sleep(0.1)

                    # Send to Perchance
                    try:
                        response = requests.post('https://perchance.org/new-image-gen-by-rs118',
                                                json={'prompt': prompt, 'orientation': orientation})
                        
                        if response.status_code == 200:
                            base64_data = response.content.decode('utf-8')
                            image_url = f"data:image/jpeg;base64,{base64_data}"
                            self.webView.load(QUrl(image_url))
                            
                            # Success message
                            QMessageBox.information(self, "Success!", 
                                    f"Image {i+1}/{num_images} generated successfully!")
                            self.status_label.setText(f"Image {i+1}/{num_images} complete. Ready to open.")
                        else:
                            error_text = response.text[:500]  # Truncate long errors
                            print(f"API Error {response.status_code}: {error_text}")
                            QMessageBox.critical(self, "Error", f"Failed to generate image {i+1}")
                    except Exception as e:
                        print(f"API Error: {e}")
                        QMessageBox.critical(self, "Error", f"Failed to get image from Perchance: {str(e)}")

        except Exception as e:
            print(f"Unexpected error in generate_image: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")


class MainWindow(QMainWindow):
    """Main window for launching the web browser"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Perchance Image Generation Browser')
        self.resize(800, 600)
        self.setMinimumSize(800, 600)

        # Create and show the web browser
        browser = WebBrowser()
        browser.show()
        self.webbrowser = browser

        # Add status bar
        status_label = QLabel("Ready\nPress 'Generate' to create images")
        self.setStatusBar(status_label)
        self.setStatusBarAlwaysActive = True

    def show_browser(self):
        """Show the web browser instance"""
        if not hasattr(self, 'webbrowser'):
            print("No browser window to show")
            return

        # If browser already visible, just show its contents
        if self.webbrowser.isVisible():
            self.webbrowser.show()
            self.webbrowser.raise_()
            self.webwindow.activateWindow()
            return

        # Otherwise, create a new browser instance
        browser = WebBrowser()
        browser.show()
        browser.raise_()
        browser.activateWindow()

        self.webbrowser = browser

    def open_browser(self):
        """Open the browser instance"""
        self.show_browser()


def openclaw_run():
    """Open a terminal-based web browser for OpenClaw integration"""
    app = QApplication(sys.argv)

    # Get current working directory
    cwd = os.getcwd()

    # Create the web browser
    browser = WebBrowser()
    browser.setCentralWidget(browser.webView)
    browser.setFixedHeight(600)
    browser.setFixedWidth(800)

    # Add controls for inputs
    prompt_label = QLabel("Enter prompt:")
    prompt_input = QLineEdit()
    prompt_input.setFixedWidth(400)
    prompt_input.setTextPlaceholder("Type a detailed prompt here...")
    prompt_input.returnPressed.connect(browser.generate_image)

    num_images_label = QLabel("Images:")
    num_images_input = QLineEdit("1")

    orientation_label = QLabel("Orientation:")
    orientation_input = QLineEdit("landscape")

    submit_btn = QPushButton("Generate Image")
    submit_btn.clicked.connect(browser.generate_image)
    submit_btn.setDefault(True)

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(prompt_label)
    layout.addWidget(prompt_input)
    layout.addWidget(num_images_label)
    layout.addWidget(num_images_input)
    layout.addWidget(orientation_label)
    layout.addWidget(orientation_input)
    layout.addWidget(submit_btn)
    layout.addStretch()

    # Set layout
    browser.setLayout(layout)

    # Run the browser
    browser.show()
    browser.setFixedSize(800, 600)
    browser.setCentralWidget(browser.webView)
    browser.raise_()
    browser.activateWindow()

    app.exec_()


if __name__ == '__main__':
    # Open the terminal browser in OpenClaw
    if len(sys.argv) > 0 and sys.argv[1] == '--terminal':
        openclaw_run()
    else:
        browser = WebBrowser()
        browser.show()
        sys.exit(app.exec_())
