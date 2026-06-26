(function() {
    var navItems = document.querySelectorAll('.report-nav .nav-item[href]');
    if (!navItems.length) return;
    var sections = [];
    navItems.forEach(function(a) {
        var id = a.getAttribute('href').replace('#', '');
        var el = document.getElementById(id);
        if (el) sections.push({ el: el, link: a });
    });
    function updateActive() {
        var scrollTop = window.scrollY + 80;
        var active = null;
        for (var i = sections.length - 1; i >= 0; i--) {
            if (sections[i].el.offsetTop <= scrollTop) { active = sections[i]; break; }
        }
        navItems.forEach(function(a) { a.classList.remove('active'); });
        if (active) active.link.classList.add('active');
    }
    window.addEventListener('scroll', updateActive, { passive: true });
    updateActive();
})();
