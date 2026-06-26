#!/usr/bin/env python3
"""Calculator Display for Wayland/Linux - 显示数字窗口"""

import sys
import os

os.environ.setdefault('DISPLAY', ':0')

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, Pango

def show_number(number):
    app = Gtk.Application()
    
    def on_activate(app):
        window = Gtk.ApplicationWindow(application=app)
        window.set_title("Calculator")
        window.set_default_size(400, 200)
        
        # Main box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(30)
        vbox.set_margin_bottom(30)
        vbox.set_margin_start(30)
        vbox.set_margin_end(30)
        
        # Label with number
        label = Gtk.Label()
        label.set_text(str(number))
        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.CENTER)
        
        # Set CSS for big font
        css = """
            label {
                font: 72px sans-serif;
            }
        """
        provider = Gtk.CssProvider()
        provider.load_from_string(css)
        label.get_style_context().add_provider(provider, 600)
        
        vbox.append(label)
        window.set_child(vbox)
        
        # Present window
        window.present()
    
    app.connect('activate', on_activate)
    app.run()

if __name__ == '__main__':
    number = sys.argv[1] if len(sys.argv) > 1 else '520'
    show_number(number)
