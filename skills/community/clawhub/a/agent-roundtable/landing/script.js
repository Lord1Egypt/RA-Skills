document.querySelectorAll('.copy').forEach((button) => {
      button.addEventListener('click', async () => {
        const text = button.dataset.copy || 'pip install agent-roundtable';
        try { await navigator.clipboard.writeText(text); button.textContent = 'Copied'; }
        catch (error) { button.textContent = 'Copy manually'; }
        window.setTimeout(() => { button.textContent = 'Copy'; }, 1500);
      });
    });
